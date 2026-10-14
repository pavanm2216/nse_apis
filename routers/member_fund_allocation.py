from fastapi import APIRouter, HTTPException
import httpx
from http_client import get_nse_client
import logging

from auth.nse_auth import get_auth_headers
from config import settings
from schemas.member_fund_allocation import (
    MemberFundOrderWiseRequest,
    MemberFundAgeWiseRequest,
    MemberFundAllocationResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Member Fund Allocation Reports"])

NSE_ORDER_WISE_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/reports/MEMBER_FUND_ALLOCATION/ORDER_WISE"
NSE_AGE_WISE_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/reports/MEMBER_FUND_ALLOCATION/AGE_WISE"


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


@router.post("/member-fund-allocation/order-wise", response_model=MemberFundAllocationResponse)
async def member_fund_order_wise(payload: MemberFundOrderWiseRequest):
    logger.info(f"Sending to NSE URL: {NSE_ORDER_WISE_URL}")
    return await _fetch_report(NSE_ORDER_WISE_URL, payload.model_dump(exclude_none=True))


@router.post("/member-fund-allocation/age-wise", response_model=MemberFundAllocationResponse)
async def member_fund_age_wise(payload: MemberFundAgeWiseRequest):
    logger.info(f"Sending to NSE URL: {NSE_AGE_WISE_URL}")
    return await _fetch_report(NSE_AGE_WISE_URL, payload.model_dump(exclude_none=True))
