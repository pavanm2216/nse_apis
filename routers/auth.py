from fastapi import APIRouter, HTTPException, Depends
import logging
import httpx
from datetime import datetime, timezone, timedelta
from jose import jwt

from auth.nse_auth import get_auth_headers
from auth.dependencies import require_auth
from config import settings
from schemas.auth import LoginRequest, LoginResponse
from http_client import get_nse_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
async def nse_login(payload: LoginRequest):
    if payload.username != settings.APP_USERNAME or payload.password != settings.APP_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    token = jwt.encode(
        {"sub": payload.username, "exp": expire},
        settings.JWT_SECRET,
        algorithm="HS256",
    )

    logger.info(f"Login successful for user: {payload.username}")
    return LoginResponse(
        status="200",
        message="Authentication successful",
        access_token=token,
        token_type="Bearer",
    )


@router.get("/debug/outbound-ip", tags=["Auth"], include_in_schema=False, dependencies=[Depends(require_auth)])
async def debug_outbound_ip():
    """
    Safe diagnostic endpoint — checks what IP NSE sees from this server.
    Calls a public IP echo service through the same HTTP client used for NSE.
    Never logs or returns credentials.
    """
    headers = get_auth_headers()
    auth_scheme = headers.get("Authorization", "").split(" ")[0]
    member_id_present = "memberId" in headers

    try:
        async with get_nse_client(10) as client:
            ip_response = await client.get("https://api.ipify.org?format=json")
            outbound_ip = ip_response.json().get("ip", "unknown")
    except Exception as e:
        outbound_ip = f"error: {e}"

    logger.info(f"[debug] auth_scheme={auth_scheme} memberId_present={member_id_present} outbound_ip={outbound_ip}")
    logger.info(f"[debug] NSE_BASE_URL={settings.NSE_BASE_URL} NSE_PROXY={'set' if settings.NSE_PROXY else 'NOT SET'}")
    logger.info(f"[debug] NSE_LOGIN_USER_ID={settings.NSE_LOGIN_USER_ID} NSE_MEMBER_ID={settings.NSE_MEMBER_ID}")

    return {
        "outbound_ip": outbound_ip,
        "auth_scheme": auth_scheme,
        "member_id_present": member_id_present,
        "nse_base_url": settings.NSE_BASE_URL,
        "proxy_configured": bool(settings.NSE_PROXY),
        "nse_login_user_id": settings.NSE_LOGIN_USER_ID,
        "nse_member_id": settings.NSE_MEMBER_ID,
    }
