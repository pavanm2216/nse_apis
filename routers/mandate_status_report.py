from fastapi import APIRouter, HTTPException
import httpx
from http_client import get_nse_client
import logging

from auth.nse_auth import get_auth_headers
from config import settings
from schemas.mandate_status_report import MandateStatusReportRequest, MandateStatusReportResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Mandate Status Report"])

NSE_MANDATE_STATUS_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/reports/MANDATE_STATUS"


@router.post("/mandate-status", response_model=MandateStatusReportResponse)
async def mandate_status_report(payload: MandateStatusReportRequest):
    logger.info(f"Sending to NSE URL: {NSE_MANDATE_STATUS_URL}")

    try:
        async with get_nse_client(60) as client:
            response = await client.post(
                NSE_MANDATE_STATUS_URL,
                headers=get_auth_headers(),
                json=payload.model_dump(exclude_none=True)
            )
    except httpx.ConnectError as e:
        raise HTTPException(status_code=502, detail=f"Cannot connect to NSE: {e}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="NSE request timed out")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"NSE request failed: {e}")

    logger.info(f"NSE Response status: {response.status_code}")
    logger.info(f"NSE Response body: {response.text[:500]}")

    if response.status_code == 403:
        raise HTTPException(status_code=403, detail="NSE authentication failed")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    try:
        return response.json()
    except Exception:
        raise HTTPException(status_code=502, detail=f"NSE returned invalid JSON: {response.text[:500]}")
