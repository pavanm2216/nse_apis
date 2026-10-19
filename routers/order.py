from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx
from http_client import get_nse_client, raise_for_nse_error, handle_nse_request_error
import logging

from database import get_db
from auth.nse_auth import get_auth_headers
from config import settings
from models.order import OrderTransaction
from schemas.order import OrderEntryRequest, OrderEntryResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/order", tags=["Order Entry"])

NSE_ORDER_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/transaction/NORMAL"

_KNOWN_FIELDS = {c.name for c in OrderTransaction.__table__.columns} - {"id", "created_at", "updated_at"}

# NSE status values that indicate a successfully placed order
_SUCCESS_STATUSES = {"NEW", "VALID"}


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

    logger.info("Sending %s order(s) to NSE", len(nse_payload["transaction_details"]))

    try:
        async with get_nse_client(60) as client:
            response = await client.post(
                NSE_ORDER_URL,
                headers=get_auth_headers(),
                json=nse_payload
            )
    except Exception as e:
        handle_nse_request_error(e)

    logger.info("NSE order response status: %s", response.status_code)

    raise_for_nse_error(response)

    try:
        nse_response = response.json()
    except Exception:
        raise HTTPException(status_code=502, detail=f"NSE returned invalid JSON: {response.text[:200]}")

    transaction_details = nse_response.get("transaction_details", [])
    saved, failed = 0, []

    try:
        for record in transaction_details:
            trxn_order_id = (record.get("trxn_order_id") or "").strip()
            trxn_status = (record.get("trxn_status") or "").strip().upper()

            if trxn_status not in _SUCCESS_STATUSES:
                logger.warning("Order not saved — trxn_status=%s", trxn_status)
                failed.append({"trxn_order_id": trxn_order_id, "trxn_status": trxn_status, "trxn_remark": record.get("trxn_remark")})
                continue

            db_data = {
                k: str(v).strip() if v is not None and str(v).strip() else None
                for k, v in record.items()
                if k in _KNOWN_FIELDS
            }

            if not trxn_order_id:
                logger.warning("Skipped DB insert — trxn_order_id missing")
                continue

            # Upsert: if NSE succeeded but DB commit failed on a prior attempt,
            # a retry will update the existing row instead of duplicating it.
            existing = await db.execute(
                select(OrderTransaction).where(OrderTransaction.trxn_order_id == trxn_order_id)
            )
            existing_record = existing.scalar_one_or_none()

            if existing_record:
                for key, value in db_data.items():
                    setattr(existing_record, key, value)
                logger.info("Updated order record: trxn_order_id=<redacted>")
            else:
                db.add(OrderTransaction(**db_data))
                saved += 1
                logger.info("Inserted order record: trxn_order_id=<redacted>")

        await db.commit()
        logger.info("DB commit done. saved=%s failed=%s", saved, len(failed))
    except Exception as e:
        await db.rollback()
        logger.error("DB error after NSE success: %s — NSE already accepted the order(s)", type(e).__name__)
        raise HTTPException(
            status_code=500,
            detail="NSE accepted the order but DB save failed. Do not retry — check trxn_order_id with NSE order status API."
        )

    return OrderEntryResponse(**nse_response)
