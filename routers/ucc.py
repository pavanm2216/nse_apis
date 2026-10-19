from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx
from http_client import get_nse_client, raise_for_nse_error, handle_nse_request_error
import logging

from database import get_db
from auth.nse_auth import get_auth_headers
from config import settings
from models.ucc import UCCRegistration
from schemas.ucc import UCCRegistrationRequest, UCCRegistrationResponse, UCCDetail, UCCDetailResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ucc", tags=["UCC Registration"])

NSE_UCC_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/registration/CLIENTCOMMON183"

# Fields defined in UCCDetail schema — unknown keys (e.g. additionalProp1) are stripped
_KNOWN_FIELDS = set(UCCDetail.model_fields.keys())


@router.post("/register", response_model=UCCRegistrationResponse)
async def register_ucc(payload: UCCRegistrationRequest, db: AsyncSession = Depends(get_db)):
    if len(payload.reg_details) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 records allowed per request")

    nse_payload = {
        "reg_details": [
            {k: v for k, v in r.model_dump().items() if k in _KNOWN_FIELDS}
            for r in payload.reg_details
        ]
    }

    logger.info("Sending UCC registration to NSE: %s records", len(nse_payload["reg_details"]))

    try:
        async with get_nse_client(30) as client:
            response = await client.post(
                NSE_UCC_URL,
                headers=get_auth_headers(),
                json=nse_payload
            )
    except Exception as e:
        handle_nse_request_error(e)

    logger.info("NSE UCC response status: %s", response.status_code)

    raise_for_nse_error(response)

    try:
        nse_response = response.json()
    except Exception:
        raise HTTPException(status_code=502, detail=f"NSE returned invalid JSON: {response.text[:200]}")

    reg_details = nse_response.get("reg_details", [])
    model_columns = {c.name for c in UCCRegistration.__table__.columns}

    success_statuses = {"REG_SUCCESS", "S"}
    saved, failed = 0, []

    try:
        for record in reg_details:
            client_code = (record.get("client_code") or "").strip()
            reg_status = (record.get("reg_status") or "").strip().upper()

            if reg_status not in success_statuses:
                logger.warning("UCC record not saved — client_code=%s reg_status=%s", client_code, reg_status)
                failed.append({"client_code": client_code, "reg_status": reg_status, "reg_remark": record.get("reg_remark")})
                continue

            db_data = {
                k: str(v).strip() if v is not None and str(v).strip() else None
                for k, v in record.items()
                if k in model_columns
            }

            if not db_data.get("client_code"):
                logger.warning("Skipped DB insert — client_code missing in NSE response record")
                continue

            existing = await db.execute(select(UCCRegistration).where(UCCRegistration.client_code == client_code))
            existing_record = existing.scalar_one_or_none()

            if existing_record:
                for key, value in db_data.items():
                    setattr(existing_record, key, value)
                logger.info("Updated UCC record: client_code=<redacted>")
            else:
                db.add(UCCRegistration(**db_data))
                saved += 1
                logger.info("Inserted UCC record: client_code=<redacted>")

        await db.commit()
        logger.info("DB commit done. saved=%s failed=%s", saved, len(failed))
    except Exception as e:
        await db.rollback()
        logger.error("DB error: %s", type(e).__name__)
        raise HTTPException(status_code=500, detail="DB save failed")

    result = UCCRegistrationResponse(**nse_response)
    if failed:
        logger.warning("UCC partial failure: %s records failed", len(failed))
    return result
