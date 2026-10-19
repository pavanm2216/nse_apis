"""
smoke_test.py — read-only NSE connectivity check.
Calls MASTER_DOWNLOAD (NAV), CLIENT_DETAIL_REPORT, then prints whether
the UCC endpoint is reachable (does not submit a registration).

Run from the NSE directory:
    python smoke_test.py

Requires the same .env as the app. Never prints credentials or client data.
"""
import asyncio
import httpx
from urllib.parse import urlparse
import socket

from config import settings
from auth.nse_auth import get_auth_headers
from http_client import get_nse_client


def _check_proxy() -> None:
    proxy = settings.NSE_PROXY
    if not proxy:
        print("[proxy] NSE_PROXY not set — using direct connection")
        return
    parsed = urlparse(proxy)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 1080
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"[proxy] OK — tunnel listening on {host}:{port}")
    except OSError:
        print(f"[proxy] FAIL — nothing on {host}:{port}. Start SSH tunnel first.")
        raise SystemExit(1)


def _sanitize(body: dict) -> dict:
    """Return envelope fields only — no client data."""
    return {k: v for k, v in body.items() if k in ("response_status", "error_remark", "file_type", "report_type")}


async def _post(client: httpx.AsyncClient, label: str, url: str, payload: dict) -> None:
    print(f"\n[{label}]")
    print(f"  URL: {url}")
    try:
        r = await client.post(url, headers=get_auth_headers(), json=payload)
        print(f"  HTTP: {r.status_code}")
        if r.headers.get("content-type", "").startswith("application/json"):
            print(f"  envelope: {_sanitize(r.json())}")
        else:
            print(f"  content-type: {r.headers.get('content-type')} len={len(r.content)}")
    except httpx.ConnectError as e:
        print(f"  CONNECT ERROR: {e!r} | cause: {e.__cause__!r}")
    except httpx.TimeoutException:
        print("  TIMEOUT")


async def main() -> None:
    _check_proxy()
    print(f"\nNSE_BASE_URL : {settings.NSE_BASE_URL}")
    print(f"NSE_MEMBER_ID: {settings.NSE_MEMBER_ID}")
    print(f"NSE_LOGIN_USER_ID: {settings.NSE_LOGIN_USER_ID}")

    base = settings.NSE_BASE_URL

    async with get_nse_client(30) as client:
        await _post(client, "MASTER_DOWNLOAD (NAV)",
                    f"{base}/nsemfdesk/api/v2/reports/MASTER_DOWNLOAD",
                    {"file_type": "NAV"})

        await _post(client, "CLIENT_DETAIL_REPORT",
                    f"{base}/nsemfdesk/api/v2/reports/CLIENT_DETAIL_REPORT",
                    {"from_date": "01/01/2024", "to_date": "01/01/2024"})

        # UCC — HEAD-equivalent: send minimal payload, expect 403 (role) or 200, not 502
        await _post(client, "UCC endpoint reachability (expect 403 or 200, not 502)",
                    f"{base}/nsemfdesk/api/v2/registration/CLIENTCOMMON183",
                    {"reg_details": []})


if __name__ == "__main__":
    asyncio.run(main())
