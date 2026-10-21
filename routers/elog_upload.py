from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import httpx
from http_client import get_nse_client
import logging

from auth.nse_auth import get_auth_headers
from config import settings
from schemas.elog_upload import ELOGUploadRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/elog", tags=["ELOG Upload"])

NSE_ELOG_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/registration/eLOG"


@router.post("/upload")
async def upload_elog(payload: ELOGUploadRequest):
    logger.info(f"Sending to NSE URL: {NSE_ELOG_URL}")

    try:
        async with get_nse_client(60) as client:
            response = await client.post(
                NSE_ELOG_URL,
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
    logger.info(f"NSE Response body: {response.text}")

    if response.status_code == 403:
        raise HTTPException(status_code=403, detail="NSE authentication failed")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    try:
        return JSONResponse(content=response.json())
    except Exception:
        raise HTTPException(status_code=502, detail=f"NSE returned invalid JSON: {response.text[:500]}")
