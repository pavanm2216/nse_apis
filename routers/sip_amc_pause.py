from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from http_client import get_nse_client
import logging

from database import get_db
from auth.nse_auth import get_auth_headers
from config import settings
from models.sip_amc_pause import SIPAmcPause
from schemas.sip_amc_pause import (
    SIPAmcPauseRequest, SIPAmcPauseResponse,
    SIPAmcPauseReportRequest, SIPAmcPauseReportResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sip-amc-pause", tags=["SIP AMC Pause"])

NSE_SIP_AMC_PAUSE_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/registration/SIP_AMC_PAUSE"
NSE_SIP_AMC_PAUSE_REPORT_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/reports/SIP_AMC_PAUSE"


@router.post("/pause", response_model=SIPAmcPauseResponse)
async def sip_amc_pause(payload: SIPAmcPauseRequest, db: AsyncSession = Depends(get_db)):
    if len(payload.pause_data) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 SIPs allowed per request")

    nse_payload = {"pause_data": [d.model_dump(exclude={"nse_remarks", "status_flag", "request_id"}) for d in payload.pause_data]}

    logger.info(f"Sending to NSE URL: {NSE_SIP_AMC_PAUSE_URL}")

    try:
        async with get_nse_client(60) as client:
            response = await client.post(
                NSE_SIP_AMC_PAUSE_URL,
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

    pause_data = nse_response.get("pause_data", [])
    model_columns = {c.name for c in SIPAmcPause.__table__.columns}

    # Merge request data with response data for DB storage
    req_map = {d.sip_reg_no: d.model_dump() for d in payload.pause_data if d.sip_reg_no}

    try:
        for record in pause_data:
            reg_no = record.get("registration_no")
            merged = {**(req_map.get(reg_no, {})), **record}
            db_data = {
                k: str(v).strip() if v is not None and str(v).strip() else None
                for k, v in merged.items()
                if k in model_columns
            }
            db.add(SIPAmcPause(**db_data))

        await db.commit()
        logger.info(f"Saved {len(pause_data)} SIP AMC pause record(s) to DB")
    except Exception as e:
        await db.rollback()
        logger.error(f"DB error: {e}")
        raise HTTPException(status_code=500, detail=f"DB save failed: {e}")

    return nse_response


@router.post("/report", response_model=SIPAmcPauseReportResponse)
async def sip_amc_pause_report(payload: SIPAmcPauseReportRequest):
    nse_payload = payload.model_dump()

    logger.info(f"Sending to NSE URL: {NSE_SIP_AMC_PAUSE_REPORT_URL}")

    try:
        async with get_nse_client(60) as client:
            response = await client.post(
                NSE_SIP_AMC_PAUSE_REPORT_URL,
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
        return response.json()
    except Exception:
        raise HTTPException(status_code=502, detail=f"NSE returned invalid JSON: {response.text[:500]}")
