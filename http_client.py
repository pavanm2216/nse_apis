import httpx
from config import settings

# When NSE_PROXY is set in .env, all outgoing NSE calls go through it
# so NSE sees requests coming from 165.22.218.229 (the whitelisted IP)
# Set in .env: NSE_PROXY=socks5://127.0.0.1:1080

def get_nse_client(total_timeout: int = 60) -> httpx.AsyncClient:
    timeout = httpx.Timeout(total_timeout, connect=10.0)
    proxy = settings.NSE_PROXY or None
    if proxy:
        return httpx.AsyncClient(proxy=proxy, timeout=timeout)
    return httpx.AsyncClient(timeout=timeout)
