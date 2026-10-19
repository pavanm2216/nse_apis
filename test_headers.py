import asyncio
import httpx
from auth.nse_auth import get_auth_headers
from config import settings


async def test(label: str, url: str, body: dict):
    headers = get_auth_headers()
    proxy = settings.NSE_PROXY or None
    print(f"\n[{label}]")
    print(f"  URL   : {url}")
    print(f"  Proxy : {'set (' + proxy + ')' if proxy else 'NOT SET — direct from laptop'}")
    try:
        async with httpx.AsyncClient(proxy=proxy, timeout=30, trust_env=False) as client:
            r = await client.post(url, headers=headers, json=body)
        print(f"  HTTP  : {r.status_code}")
        ct = r.headers.get("content-type", "")
        if "application/json" in ct:
            data = r.json()
            print(f"  response_status : {data.get('response_status')}")
            print(f"  error_remark    : {data.get('error_remark')}")
        else:
            print(f"  content-type: {ct}  len={len(r.content)}")
    except Exception as e:
        print(f"  ERROR : {e!r}")
        print(f"  cause : {e.__cause__!r}")


async def main():
    base = settings.NSE_BASE_URL
    await test(
        "MASTER_DOWNLOAD (NAV) — known-good control",
        f"{base}/nsemfdesk/api/v2/reports/MASTER_DOWNLOAD",
        {"file_type": "NAV"},
    )
    await test(
        "UCC CLIENTCOMMON183 — empty payload, just testing reachability",
        f"{base}/nsemfdesk/api/v2/registration/CLIENTCOMMON183",
        {"reg_details": []},
    )


asyncio.run(main())
