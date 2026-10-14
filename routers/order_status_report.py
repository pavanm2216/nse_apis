from fastapi import APIRouter, HTTPException
import httpx
from http_client import get_nse_client
import logging

from auth.nse_auth import get_auth_headers
from config import settings
from schemas.order_status_report import OrderStatusRequest, OrderStatusResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Order Status Reports"])

NSE_PROV_ORDERS_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/reports/PROV_ORDERS"
NSE_ORDER_STATUS_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/reports/ORDER_STATUS"


async def _fetch_report(url: str, payload: OrderStatusRequest) -> dict:
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


@router.post("/provisional-orders", response_model=OrderStatusResponse)
async def provisional_orders(payload: OrderStatusRequest):
    logger.info(f"Sending to NSE URL: {NSE_PROV_ORDERS_URL}")
    return await _fetch_report(NSE_PROV_ORDERS_URL, payload)


@router.post("/order-status", response_model=OrderStatusResponse)
async def order_status(payload: OrderStatusRequest):
    logger.info(f"Sending to NSE URL: {NSE_ORDER_STATUS_URL}")
    return await _fetch_report(NSE_ORDER_STATUS_URL, payload)
