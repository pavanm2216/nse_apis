from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from http_client import get_nse_client
import logging

from database import get_db
from auth.nse_auth import get_auth_headers
from config import settings
from models.order import OrderTransaction
from schemas.order import OrderEntryRequest, OrderEntryResponse, OrderRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/order", tags=["Order Entry"])

NSE_ORDER_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/transaction/NORMAL"

# Map column name → max length for VARCHAR(n) columns that NSE may overflow
_VARCHAR_LIMITS: dict[str, int] = {
    "trxn_type":          1,
    "demat_physical":     1,
    "kyc_flag":           1,
    "euin_declaration":   1,
    "min_redemption_flag":1,
    "dpc_flag":           1,
    "all_units":          1,
}


def _check_oversized(record: dict) -> list[str]:
    return [
        f"{col}={record[col]!r} exceeds VARCHAR({limit})"
        for col, limit in _VARCHAR_LIMITS.items()
        if col in record and record[col] and len(str(record[col])) > limit
    ]


@router.post("/entry", response_model=OrderEntryResponse)
async def order_entry(payload: OrderEntryRequest, db: AsyncSession = Depends(get_db)):
    if not payload.transaction_details:
        raise HTTPException(status_code=422, detail="transaction_details cannot be empty")

    if len(payload.transaction_details) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 orders allowed per request")

    nse_payload = {
        "transaction_details": [
            {k: v for k, v in d.model_dump(exclude_none=True).items() if v != ""}
            for d in payload.transaction_details
        ]
    }

    logger.info(f"Sending to NSE URL: {NSE_ORDER_URL}")

    try:
        async with get_nse_client(60) as client:
            response = await client.post(
                NSE_ORDER_URL,
                headers=get_auth_headers(),
                json=nse_payload
            )
    except httpx.ConnectError as e:
        raise HTTPException(status_code=502, detail=f"Cannot connect to NSE: {e}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="NSE request timed out")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"NSE request failed: {e}")

    logger.info(f"NSE Response status: {response.status_code}")
    logger.info(f"NSE Response body: {response.text}")

    if response.status_code == 403:
        raise HTTPException(status_code=403, detail=f"NSE 403: {response.text}")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    try:
        nse_response = response.json()
    except Exception:
        raise HTTPException(status_code=502, detail=f"NSE returned invalid JSON: {response.text[:500]}")

    transaction_details = nse_response.get("transaction_details", [])

    # Detect oversized values before attempting DB insert
    oversized_errors: list[str] = []
    for record in transaction_details:
        oversized_errors.extend(_check_oversized(record))
    if oversized_errors:
        logger.error(f"NSE response contains oversized values: {oversized_errors}")
        raise HTTPException(
            status_code=502,
            detail=f"NSE response contains values exceeding column limits: {'; '.join(oversized_errors)}"
        )

    model_columns = {c.name for c in OrderTransaction.__table__.columns}

    try:
        for record in transaction_details:
            db_data = {
                k: str(v).strip() if v is not None and str(v).strip() else None
                for k, v in record.items()
                if k in model_columns
            }
            db.add(OrderTransaction(**db_data))

        await db.commit()
        logger.info(f"Saved {len(transaction_details)} order(s) to DB")
    except Exception as e:
        await db.rollback()
        logger.error(f"DB error: {e}")
        raise HTTPException(status_code=500, detail=f"DB save failed: {e}")

    return OrderEntryResponse(**nse_response)
