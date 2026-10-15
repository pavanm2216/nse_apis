from fastapi import APIRouter, HTTPException
import httpx
from http_client import get_nse_client
import logging

from auth.nse_auth import get_auth_headers
from config import settings
from schemas.misc_services import (
    EKYCRegRequest, EKYCRegResponse,
    PurchasePaymentRequest, PurchasePaymentResponse,
    UPIStatusCheckRequest, UPIStatusCheckResponse,
    SWPCancellationRequest, SWPCancellationResponse,
    SIPXSIPPauseRequest, SIPXSIPPauseResponse,
    ClientMasterReportRequest, ClientMasterReportResponse,
    ChangeAPISecretResponse,
    NFTNOMRequest, NFTNOMResponse,
    NFTCOARequest, NFTCODRequest, NFTCOBRequest, NFTResponse,
    NFTCOCRequest, NFTCOFRequest, NFTCOMRequest,
    NFTImageUploadRequest, NFTImageUploadResponse,
    SIPModRequest, SIPModResponse,
    KycFreshRegisterRequest, KycFreshRegisterResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Misc Services"])

NSE_EKYC_REG_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v1/EKYC/EKYCREG"
NSE_PURCHASE_PAYMENT_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/payments/purchase_payment"
NSE_UPI_STATUS_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/payments/upi_status_check"
NSE_SWP_CAN_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/cancellation/SWP_CAN"
NSE_XSIP_PAUSE_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/registration/XSIP_PAUSE"
NSE_CLIENT_MASTER_REPORT_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/reports/client_master_report"
NSE_CHANGE_API_SECRET_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/admin/CHANGE_API_SECRET"
NSE_NFT_NOM_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v1/NFT/NOM"
NSE_NFT_COA_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v1/NFT/COA"
NSE_NFT_COD_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v1/NFT/COD"
NSE_NFT_COB_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v1/NFT/COB"
NSE_NFT_COC_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v1/NFT/COC"
NSE_NFT_COF_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v1/NFT/COF"
NSE_NFT_COM_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v1/NFT/COM"
NSE_NFT_IMAGE_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/fileupload/NFTIMAGE"
NSE_SIP_MOD_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/modification/product/SIP_MOD"
NSE_XSIP_MOD_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/modification/product/XSIP_MOD"
NSE_KYC_FRESH_REG_URL = f"{settings.NSE_BASE_URL}/nsemfdesk/api/v2/registration/KYC_FRESH_REGISTER"


async def _post(url: str, payload: dict) -> dict:
    try:
        async with get_nse_client(60) as client:
            response = await client.post(url, headers=get_auth_headers(), json=payload)
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


@router.post("/ekyc/register", response_model=EKYCRegResponse)
async def ekyc_register(payload: EKYCRegRequest):
    logger.info(f"Sending to NSE URL: {NSE_EKYC_REG_URL}")
    return await _post(NSE_EKYC_REG_URL, payload.model_dump())


@router.post("/payments/purchase", response_model=PurchasePaymentResponse)
async def purchase_payment(payload: PurchasePaymentRequest):
    logger.info(f"Sending to NSE URL: {NSE_PURCHASE_PAYMENT_URL}")
    return await _post(NSE_PURCHASE_PAYMENT_URL, payload.model_dump(exclude_none=True))


@router.post("/payments/upi-status", response_model=UPIStatusCheckResponse)
async def upi_status_check(payload: UPIStatusCheckRequest):
    logger.info(f"Sending to NSE URL: {NSE_UPI_STATUS_URL}")
    return await _post(NSE_UPI_STATUS_URL, payload.model_dump())


@router.post("/cancellation/swp", response_model=SWPCancellationResponse)
async def swp_cancellation(payload: SWPCancellationRequest):
    logger.info(f"Sending to NSE URL: {NSE_SWP_CAN_URL}")
    return await _post(NSE_SWP_CAN_URL, payload.model_dump(exclude_none=True))


@router.post("/registration/sip-xsip-pause", response_model=SIPXSIPPauseResponse)
async def sip_xsip_pause(payload: SIPXSIPPauseRequest):
    logger.info(f"Sending to NSE URL: {NSE_XSIP_PAUSE_URL}")
    return await _post(NSE_XSIP_PAUSE_URL, payload.model_dump(exclude_none=True))


@router.post("/reports/client-master", response_model=ClientMasterReportResponse)
async def client_master_report(payload: ClientMasterReportRequest):
    logger.info(f"Sending to NSE URL: {NSE_CLIENT_MASTER_REPORT_URL}")
    return await _post(NSE_CLIENT_MASTER_REPORT_URL, payload.model_dump(exclude_none=True))


@router.post("/admin/change-api-secret", response_model=ChangeAPISecretResponse)
async def change_api_secret():
    logger.info(f"Sending to NSE URL: {NSE_CHANGE_API_SECRET_URL}")
    return await _post(NSE_CHANGE_API_SECRET_URL, {})


@router.post("/nft/nominee", response_model=NFTNOMResponse)
async def nft_nom_register(payload: NFTNOMRequest):
    logger.info(f"Sending to NSE URL: {NSE_NFT_NOM_URL}")
    return await _post(NSE_NFT_NOM_URL, payload.to_nse_payload())


@router.post("/nft/change-of-bank", response_model=NFTResponse)
async def nft_coa(payload: NFTCOARequest):
    logger.info(f"Sending to NSE URL: {NSE_NFT_COA_URL}")
    return await _post(NSE_NFT_COA_URL, payload.to_nse_payload())


@router.post("/nft/change-of-dividend", response_model=NFTResponse)
async def nft_cod(payload: NFTCODRequest):
    logger.info(f"Sending to NSE URL: {NSE_NFT_COD_URL}")
    return await _post(NSE_NFT_COD_URL, payload.to_nse_payload())


@router.post("/nft/change-of-broker", response_model=NFTResponse)
async def nft_cob(payload: NFTCOBRequest):
    logger.info(f"Sending to NSE URL: {NSE_NFT_COB_URL}")
    return await _post(NSE_NFT_COB_URL, payload.to_nse_payload())


@router.post("/nft/change-of-contact", response_model=NFTResponse)
async def nft_coc(payload: NFTCOCRequest):
    logger.info(f"Sending to NSE URL: {NSE_NFT_COC_URL}")
    return await _post(NSE_NFT_COC_URL, payload.to_nse_payload())


@router.post("/nft/consolidation-of-folio", response_model=NFTResponse)
async def nft_cof(payload: NFTCOFRequest):
    logger.info(f"Sending to NSE URL: {NSE_NFT_COF_URL}")
    return await _post(NSE_NFT_COF_URL, payload.to_nse_payload())


@router.post("/nft/change-of-bank-single", response_model=NFTResponse)
async def nft_com(payload: NFTCOMRequest):
    logger.info(f"Sending to NSE URL: {NSE_NFT_COM_URL}")
    return await _post(NSE_NFT_COM_URL, payload.to_nse_payload())


@router.post("/nft/image-upload", response_model=NFTImageUploadResponse)
async def nft_image_upload(payload: NFTImageUploadRequest):
    logger.info(f"Sending to NSE URL: {NSE_NFT_IMAGE_URL}")
    return await _post(NSE_NFT_IMAGE_URL, payload.model_dump())


@router.post("/modification/sip", response_model=SIPModResponse)
async def sip_modification(payload: SIPModRequest):
    logger.info(f"Sending to NSE URL: {NSE_SIP_MOD_URL}")
    return await _post(NSE_SIP_MOD_URL, payload.model_dump(exclude_none=True))


@router.post("/modification/xsip", response_model=SIPModResponse)
async def xsip_modification(payload: SIPModRequest):
    logger.info(f"Sending to NSE URL: {NSE_XSIP_MOD_URL}")
    return await _post(NSE_XSIP_MOD_URL, payload.model_dump(exclude_none=True))


@router.post("/registration/kyc-fresh-register", response_model=KycFreshRegisterResponse)
async def kyc_fresh_register(payload: KycFreshRegisterRequest):
    logger.info(f"Sending to NSE URL: {NSE_KYC_FRESH_REG_URL}")
    return await _post(NSE_KYC_FRESH_REG_URL, payload.model_dump(exclude_none=True))
