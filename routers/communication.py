from fastapi import APIRouter, HTTPException
import httpx
from http_client import get_nse_client
import logging

from auth.nse_auth import get_auth_headers
from config import settings
from schemas.communication import GetLinkRequest, GetLinkResponse, ResendCommRequest, ResendCommResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/communication", tags=["Communication"])

NSE_GET_LINK_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/reports/GET_LINK"
NSE_RESEND_COMM_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/registration/RESEND_COMM"


async def _post(url: str, payload: dict) -> dict:
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
    logger.info(f"NSE Response body: {response.text}")

    if response.status_code == 403:
        raise HTTPException(status_code=403, detail="NSE authentication failed")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    try:
        return response.json()
    except Exception:
        raise HTTPException(status_code=502, detail=f"NSE returned invalid JSON: {response.text[:500]}")


@router.post("/get-link", response_model=GetLinkResponse)
async def get_link(payload: GetLinkRequest):
    logger.info(f"Sending to NSE URL: {NSE_GET_LINK_URL}")
    return await _post(NSE_GET_LINK_URL, payload.model_dump())


@router.post("/resend", response_model=ResendCommResponse)
async def resend_comm(payload: ResendCommRequest):
    logger.info(f"Sending to NSE URL: {NSE_RESEND_COMM_URL}")
    return await _post(NSE_RESEND_COMM_URL, payload.model_dump())
