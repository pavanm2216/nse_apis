from fastapi import APIRouter, HTTPException
import httpx
import logging

from auth.nse_auth import get_auth_headers_for_credentials
from config import settings
from http_client import get_nse_client
from schemas.auth import LoginRequest, LoginResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])

# NSE has no dedicated login endpoint — auth is validated per-request via headers.
# We probe with a lightweight read-only endpoint to verify credentials.
NSE_AUTH_PROBE_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/reports/ORDER_STATUS"

PROBE_PAYLOAD = {
    "from_date": "01/01/2099",
    "to_date": "01/01/2099",
    "trans_type": "",
    "order_type": "",
    "sub_order_type": "",
}


async def _probe(headers: dict) -> httpx.Response:
    try:
        async with get_nse_client(30) as client:
            return await client.post(NSE_AUTH_PROBE_URL, headers=headers, json=PROBE_PAYLOAD)
    except httpx.ConnectError as e:
        raise HTTPException(status_code=502, detail=f"Cannot connect to NSE: {e}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="NSE login request timed out")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"NSE request failed: {e}")


@router.post("/login", response_model=LoginResponse)
async def nse_login(payload: LoginRequest):
    logger.info(f"NSE auth check — user: {payload.username}, member: {settings.NSE_MEMBER_ID}")

    # Attempt 1: NSE_API_SECRET from .env as AES secret (standard NSE flow)
    response = await _probe(get_auth_headers_for_credentials(
        user_id=payload.username,
        api_secret=settings.NSE_API_SECRET,
        license_key=settings.NSE_API_LICENSE_KEY,
        member_id=settings.NSE_MEMBER_ID,
    ))
    logger.info(f"Attempt 1 (env api_secret) — NSE status: {response.status_code}")

    if response.status_code == 200:
        return LoginResponse(status="200", message="Authentication successful")

    # Attempt 2: caller's password as AES secret (some NSE UAT setups use Member Desk password)
    response2 = await _probe(get_auth_headers_for_credentials(
        user_id=payload.username,
        api_secret=payload.password,
        license_key=settings.NSE_API_LICENSE_KEY,
        member_id=settings.NSE_MEMBER_ID,
    ))
    logger.info(f"Attempt 2 (password as api_secret) — NSE status: {response2.status_code}")

    if response2.status_code == 200:
        return LoginResponse(status="200", message="Authentication successful")

    # Attempt 3: caller's password as both AES secret AND license key
    response3 = await _probe(get_auth_headers_for_credentials(
        user_id=payload.username,
        api_secret=payload.password,
        license_key=payload.password,
        member_id=settings.NSE_MEMBER_ID,
    ))
    logger.info(f"Attempt 3 (password as secret+key) — NSE status: {response3.status_code}")

    if response3.status_code == 200:
        return LoginResponse(status="200", message="Authentication successful")

    raise HTTPException(
        status_code=403,
        detail="Invalid authorization header or IP Address not mapped with user."
    )
