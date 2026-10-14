"""Check NSE order status without logging credentials or response data.

Run from the project root: python check_order_status.py
Uses the existing settings and credentials from .env.
"""

import asyncio
import time

from config import settings
from auth.nse_auth import get_auth_headers
from http_client import get_nse_client
import httpx


async def main() -> None:
    url = (
        f"{settings.NSE_BASE_URL.rstrip('/')}"
        "/nsemfdesk/api/v2/reports/ORDER_STATUS"
    )
    payload = {
        "from_date": "12/10/2026",
        "to_date": "12/10/2026",
        "trans_type": "",
        "order_type": "",
        "sub_order_type": "",
    }

    start = time.perf_counter()
    try:
        async with get_nse_client(30) as client:
            response = await client.post(
                url, headers=get_auth_headers(), json=payload
            )

        elapsed = time.perf_counter() - start
        print("HTTP Status:", response.status_code)
        print(f"Response Time: {elapsed:.2f} seconds")
        print("Response Length:", len(response.content))

        if response.status_code == 403:
            print("Authentication or access denied.")

    except httpx.TimeoutException as exc:
        print("NSE Timeout:", type(exc).__name__)
        print(f"Time Waited: {time.perf_counter() - start:.2f} seconds")
    except httpx.RequestError as exc:
        print("Connection Error:", type(exc).__name__)


if __name__ == "__main__":
    asyncio.run(main())
