from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx
from http_client import get_nse_client
import logging

from database import get_db
from auth.nse_auth import get_auth_headers
from config import settings
from models.ucc import UCCRegistration
from schemas.ucc import UCCRegistrationRequest, UCCRegistrationResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ucc", tags=["UCC Registration"])

NSE_UCC_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/registration/CLIENTCOMMON"


@router.post("/register", response_model=UCCRegistrationResponse)
async def register_ucc(payload: UCCRegistrationRequest, db: AsyncSession = Depends(get_db)):
    if len(payload.reg_details) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 records allowed per request")

    nse_payload = {
        "reg_details": [
            {k: v for k, v in r.model_dump(exclude_none=True).items() if v != ""}
            for r in payload.reg_details
        ]
    }

    logger.info(f"Sending to NSE URL: {NSE_UCC_URL}")

    try:
        async with get_nse_client(30) as client:
            response = await client.post(
                NSE_UCC_URL,
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
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"NSE returned invalid JSON: {response.text[:500]}")

    reg_details = nse_response.get("reg_details", [])
    model_columns = {c.name for c in UCCRegistration.__table__.columns}

    saved_count = 0
    try:
        for record in reg_details:
            client_code = (record.get("client_code") or "").strip()
            existing = await db.execute(select(UCCRegistration).where(UCCRegistration.client_code == client_code))
            existing_record = existing.scalar_one_or_none()

            db_data = {
                k: str(v).strip() if v is not None and str(v).strip() else None
                for k, v in record.items()
                if k in model_columns
            }

            if existing_record:
                for key, value in db_data.items():
                    setattr(existing_record, key, value)
                logger.info(f"Updated existing UCC record: {client_code}")
            else:
                if db_data.get("client_code"):
                    db.add(UCCRegistration(**db_data))
                    saved_count += 1
                    logger.info(f"Inserted new UCC record: {client_code}")
                else:
                    logger.warning("Skipped DB insert — client_code is empty in NSE response")

        await db.commit()
        logger.info(f"DB commit done. Records saved: {saved_count}")
    except Exception as e:
        await db.rollback()
        logger.error(f"DB error: {e}")
        raise HTTPException(status_code=500, detail=f"DB save failed: {e}")

    return UCCRegistrationResponse(**nse_response)
