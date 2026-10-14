from fastapi import APIRouter, HTTPException
import httpx
from http_client import get_nse_client
import logging

from auth.nse_auth import get_auth_headers
from config import settings
from schemas.statement_reports import (
    RedemptionStatementRequest,
    AllotmentStatementRequest,
    StatementReportResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Statement Reports"])

NSE_REDEMPTION_STATEMENT_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/reports/REDEMPTION_STATEMENT"
NSE_ALLOTMENT_STATEMENT_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/reports/ALLOTMENT_STATEMENT"


async def _fetch_report(url: str, payload: dict) -> dict:
    try:
        async with get_nse_client(60) as client:
            response = await client.post(url, headers=get_auth_headers(), json=payload)
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


@router.post("/redemption-statement", response_model=StatementReportResponse)
async def redemption_statement(payload: RedemptionStatementRequest):
    logger.info(f"Sending to NSE URL: {NSE_REDEMPTION_STATEMENT_URL}")
    return await _fetch_report(NSE_REDEMPTION_STATEMENT_URL, payload.model_dump(exclude_none=True))


@router.post("/allotment-statement", response_model=StatementReportResponse)
async def allotment_statement(payload: AllotmentStatementRequest):
    logger.info(f"Sending to NSE URL: {NSE_ALLOTMENT_STATEMENT_URL}")
    return await _fetch_report(NSE_ALLOTMENT_STATEMENT_URL, payload.model_dump(exclude_none=True))
