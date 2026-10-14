from fastapi import APIRouter, HTTPException
import httpx
from http_client import get_nse_client
import logging

from auth.nse_auth import get_auth_headers
from config import settings
from schemas.fatca_image_upload import FATCAImageUploadRequest, FATCAImageUploadResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/fatca", tags=["FATCA Image Upload"])

NSE_FATCA_IMG_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/fileupload/FATCAIMG"


@router.post("/image-upload", response_model=FATCAImageUploadResponse)
async def upload_fatca_image(payload: FATCAImageUploadRequest):
    logger.info(f"Sending to NSE URL: {NSE_FATCA_IMG_URL}")

    try:
        async with get_nse_client(60) as client:
            response = await client.post(
                NSE_FATCA_IMG_URL,
                headers=get_auth_headers(),
                json=payload.model_dump()
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
        return response.json()
    except Exception:
        raise HTTPException(status_code=502, detail=f"NSE returned invalid JSON: {response.text[:500]}")
