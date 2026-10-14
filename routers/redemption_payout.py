from fastapi import APIRouter, HTTPException
import httpx
from http_client import get_nse_client
import logging

from auth.nse_auth import get_auth_headers
from config import settings
from schemas.redemption_payout import RedemptionPayoutRequest, RedemptionPayoutResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Redemption Payout Reports"])

NSE_REDEMPTION_PAYOUT_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/reports/REDEMPTION_PAYOUT"
NSE_REDEMPTION_PAYOUT_NON_DEMAT_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/reports/REDEMPTION_PAYOUT_NON_DEMAT"


async def _fetch_report(url: str, payload: RedemptionPayoutRequest) -> dict:
    try:
        async with get_nse_client(60) as client:
            response = await client.post(
                url,
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


@router.post("/redemption-payout", response_model=RedemptionPayoutResponse)
async def redemption_payout(payload: RedemptionPayoutRequest):
    logger.info(f"Sending to NSE URL: {NSE_REDEMPTION_PAYOUT_URL}")
    return await _fetch_report(NSE_REDEMPTION_PAYOUT_URL, payload)


@router.post("/redemption-payout-non-demat", response_model=RedemptionPayoutResponse)
async def redemption_payout_non_demat(payload: RedemptionPayoutRequest):
    logger.info(f"Sending to NSE URL: {NSE_REDEMPTION_PAYOUT_NON_DEMAT_URL}")
    return await _fetch_report(NSE_REDEMPTION_PAYOUT_NON_DEMAT_URL, payload)
