from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from http_client import get_nse_client
import logging

from database import get_db
from auth.nse_auth import get_auth_headers
from config import settings
from models.order_cancellation import OrderCancellation
from schemas.order_cancellation import OrderCancellationRequest, OrderCancellationResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/order-cancellation", tags=["Order Cancellation"])

NSE_ORDER_CAN_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/cancellation/ORDER_CAN"


@router.post("/cancel", response_model=OrderCancellationResponse)
async def cancel_order(payload: OrderCancellationRequest, db: AsyncSession = Depends(get_db)):
    if len(payload.can_data) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 orders allowed per request")

    nse_payload = {"can_data": [d.model_dump() for d in payload.can_data]}

    logger.info(f"Sending to NSE URL: {NSE_ORDER_CAN_URL}")

    try:
        async with get_nse_client(60) as client:
            response = await client.post(
                NSE_ORDER_CAN_URL,
                headers=get_auth_headers(),
                json=nse_payload
            )
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
        nse_response = response.json()
    except Exception:
        raise HTTPException(status_code=502, detail=f"NSE returned invalid JSON: {response.text[:500]}")

    # NSE returns reg_data key in response (not can_data)
    can_data = nse_response.get("reg_data", [])
    model_columns = {c.name for c in OrderCancellation.__table__.columns}

    try:
        for record in can_data:
            db_data = {
                k: str(v).strip() if v is not None and str(v).strip() else None
                for k, v in record.items()
                if k in model_columns
            }
            db.add(OrderCancellation(**db_data))

        await db.commit()
        logger.info(f"Saved {len(can_data)} order cancellation(s) to DB")
    except Exception as e:
        await db.rollback()
        logger.error(f"DB error: {e}")
        raise HTTPException(status_code=500, detail=f"DB save failed: {e}")

    return nse_response
