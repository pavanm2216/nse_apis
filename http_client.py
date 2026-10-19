import socket
from urllib.parse import urlparse
import httpx
from fastapi import HTTPException
from config import settings
import logging

logger = logging.getLogger(__name__)


def check_proxy_reachable() -> None:
    """Called at startup. Raises RuntimeError if NSE_PROXY is set but the port is not listening."""
    proxy = settings.NSE_PROXY
    if not proxy:
        return
    parsed = urlparse(proxy)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 1080
    try:
        with socket.create_connection((host, port), timeout=2):
            pass
        logger.info("NSE proxy reachable at %s:%s", host, port)
    except OSError:
        raise RuntimeError(
            f"NSE_PROXY is set to {proxy!r} but nothing is listening on {host}:{port}. "
            "Start the SSH tunnel: ssh -D 1080 -N -o ServerAliveInterval=60 root@<server>"
        )


def get_nse_client(total_timeout: int = 60) -> httpx.AsyncClient:
    timeout = httpx.Timeout(total_timeout, connect=10.0)
    proxy = settings.NSE_PROXY or None
    if proxy:
        logger.info("NSE HTTP client: using proxy (whitelisted IP routing)")
        return httpx.AsyncClient(proxy=proxy, timeout=timeout, trust_env=False)
    logger.warning("NSE HTTP client: NO proxy set — outbound IP may not be whitelisted at NSE")
    return httpx.AsyncClient(timeout=timeout, trust_env=False)


def raise_for_nse_error(response: httpx.Response) -> None:
    """Uniform HTTP-level error handling for every NSE router."""
    if response.status_code == 403:
        raise HTTPException(status_code=403, detail=f"NSE 403 — bad credentials, unmapped IP, or role not enabled: {response.text}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)


def handle_nse_request_error(e: Exception) -> None:
    """Uniform transport-level error handling for every NSE router."""
    if isinstance(e, httpx.ConnectError):
        logger.error("NSE connect error: %r | cause: %r", e, e.__cause__)
        raise HTTPException(status_code=502, detail=f"Cannot connect to NSE: {e!r}")
    if isinstance(e, httpx.TimeoutException):
        raise HTTPException(status_code=504, detail="NSE request timed out")
    raise HTTPException(status_code=502, detail=f"NSE request failed: {e!r}")
