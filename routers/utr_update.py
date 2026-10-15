from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from http_client import get_nse_client
import logging

from database import get_db
from auth.nse_auth import get_auth_headers
from config import settings
from models.utr_update import UTRUpdate
from schemas.utr_update import UTRUpdateRequest, UTRUpdateResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/utr", tags=["UTR Update"])

NSE_UTR_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/transaction/UTRUPDATE"


@router.post("/update", response_model=UTRUpdateResponse)
async def utr_update(payload: UTRUpdateRequest, db: AsyncSession = Depends(get_db)):
    if len(payload.utr_details) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 records allowed per request")

    nse_payload = {
        "utr_details": [
            {k: v for k, v in d.model_dump(exclude_none=True).items() if v != ""}
            for d in payload.utr_details
        ]
    }

    logger.info(f"Sending to NSE URL: {NSE_UTR_URL}")

    try:
        async with get_nse_client(60) as client:
            response = await client.post(
                NSE_UTR_URL,
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
        raise HTTPException(status_code=403, detail="NSE authentication failed")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    try:
        nse_response = response.json()
    except Exception:
        raise HTTPException(status_code=502, detail=f"NSE returned invalid JSON: {response.text[:500]}")

    utr_details = nse_response.get("utr_details", [])
    model_columns = {c.name for c in UTRUpdate.__table__.columns}

    try:
        for record in utr_details:
            db_data = {
                k: str(v).strip() if v is not None and str(v).strip() else None
                for k, v in record.items()
                if k in model_columns
            }
            db.add(UTRUpdate(**db_data))

        await db.commit()
        logger.info(f"Saved {len(utr_details)} UTR update(s) to DB")
    except Exception as e:
        await db.rollback()
        logger.error(f"DB error: {e}")
        raise HTTPException(status_code=500, detail=f"DB save failed: {e}")

    return nse_response
