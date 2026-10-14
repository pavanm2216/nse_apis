from fastapi import APIRouter, HTTPException
import httpx
import logging

from auth.nse_auth import get_auth_headers
from config import settings
from http_client import get_nse_client
from schemas.auth import LoginRequest, LoginResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])

NSE_AUTH_PROBE_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/reports/ORDER_STATUS"

PROBE_PAYLOAD = {
    "from_date": "01/01/2099",
    "to_date": "01/01/2099",
    "trans_type": "",
    "order_type": "",
    "sub_order_type": "",
}


@router.post("/login", response_model=LoginResponse)
async def nse_login(payload: LoginRequest):
    logger.info(f"NSE auth check — user: {payload.username}, member: {settings.NSE_MEMBER_ID}")

    try:
        async with get_nse_client(30) as client:
            response = await client.post(
                NSE_AUTH_PROBE_URL,
                headers=get_auth_headers(),
                json=PROBE_PAYLOAD
            )
    except httpx.ConnectError as e:
        raise HTTPException(status_code=502, detail=f"Cannot connect to NSE: {e}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="NSE login request timed out")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"NSE request failed: {e}")

    logger.info(f"NSE response status: {response.status_code}")
    logger.info(f"NSE response body: {response.text[:500]}")

    if response.status_code == 403:
        raise HTTPException(
            status_code=403,
            detail="Invalid authorization header or IP Address not mapped with user."
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return LoginResponse(status="200", message="Authentication successful")
