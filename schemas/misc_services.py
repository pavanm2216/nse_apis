from pydantic import BaseModel
from typing import Optional, List, Any


class EKYCRegRequest(BaseModel):
    amcCode: str
    panNo: str
    mobileNo: str
    invEmail: str


class EKYCRegResponse(BaseModel):
    link: Optional[str] = None
    message: Optional[str] = None


class PurchasePaymentRequest(BaseModel):
    payment_mode: str
    client_code: str
    order_ids: str
    mandate_id: Optional[str] = None
    bank_account_no: Optional[str] = None
    ifsc: Optional[str] = None
    cheque_no: Optional[str] = None
    cheque_date: Optional[str] = None
    vpa: Optional[str] = None
    neft_rtgs_utr_no: Optional[str] = None
    callback_url: Optional[str] = None


class PurchasePaymentResponse(BaseModel):
    payment_mode: Optional[str] = None
    client_code: Optional[str] = None
    order_ids: Optional[str] = None
    status: Optional[str] = None
    order_amount: Optional[Any] = None
    remark: Optional[str] = None
    short_url: Optional[str] = None
    basket_id: Optional[str] = None
    mandate_id: Optional[str] = None
    bank_account_no: Optional[str] = None
    ifsc: Optional[str] = None
    cheque_no: Optional[str] = None
    cheque_date: Optional[str] = None
    vpa: Optional[str] = None
    callback_url: Optional[str] = None
    neft_rtgs_utr_no: Optional[str] = None


class UPIStatusCheckRequest(BaseModel):
    nse_upi_ref_no: str
    client_code: str


class UPIStatusCheckResponse(BaseModel):
    payment_mode: Optional[str] = None
    client_code: Optional[str] = None
    bank_account_no: Optional[str] = None
    ifsc: Optional[str] = None
    vpa: Optional[str] = None
    status: Optional[str] = None
    order_amount: Optional[Any] = None
    remark: Optional[str] = None
    nse_upi_ref_no: Optional[str] = None
    upi_tran_ref_id: Optional[str] = None
    cust_ref_no: Optional[str] = None


class SWPCanItem(BaseModel):
    client_code: str
    swp_reg_no: str
    remarks: Optional[str] = None
    can_status: Optional[str] = None
    can_remark: Optional[str] = None


class SWPCancellationRequest(BaseModel):
    can_data: List[SWPCanItem]


class SWPCancellationResponse(BaseModel):
    reg_data: Optional[List[Any]] = None


class SIPPauseItem(BaseModel):
    sip_reg_no: str
    effective_date: str
    pause_flag: str
    remarks: Optional[str] = None


class SIPXSIPPauseRequest(BaseModel):
    pause_data: List[SIPPauseItem]


class SIPXSIPPauseResponse(BaseModel):
    pause_data: Optional[List[Any]] = None


class ClientMasterReportRequest(BaseModel):
    client_code: Optional[str] = None
    pan: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class ClientMasterReportResponse(BaseModel):
    response_status: str
    report_data_total: str
    report_data: Optional[List[Any]] = None
    error_remark: Optional[str] = None


class ChangeAPISecretResponse(BaseModel):
    api_secret: str


class NFTNomItem(BaseModel):
    AMC_CODE: Optional[str] = None
    FOLIO_NO: Optional[str] = None
    NCT_TYPE: Optional[str] = None
    FH_NAME: Optional[str] = None
    TAX_NUMBER: Optional[str] = None
    DOC_TYPE: Optional[str] = None
    TWOFA_AUTH: Optional[str] = None
    IMG_REF_NO: Optional[str] = None
    EMAIL: Optional[str] = None
    MOBILE_NO: Optional[str] = None
    NOM_OPT: Optional[str] = None
    NOM1_NAME: Optional[str] = None
    NOM1_RELA: Optional[str] = None
    NOM1_PER: Optional[str] = None
    NOM1_IDNO: Optional[str] = None
    NOM1_MIN_F: Optional[str] = None
    NOM1_DOB: Optional[str] = None
    NOM1_GUARD: Optional[str] = None
    NOM1_GRELA: Optional[str] = None
    NOM1_GPAN: Optional[str] = None
    NOM2_NAME: Optional[str] = None
    NOM2_RELA: Optional[str] = None
    NOM2_PER: Optional[str] = None
    NOM2_IDNO: Optional[str] = None
    NOM2_MIN_F: Optional[str] = None
    NOM2_DOB: Optional[str] = None
    NOM2_GUARD: Optional[str] = None
    NOM2_GRELA: Optional[str] = None
    NOM2_GPAN: Optional[str] = None
    NOM3_NAME: Optional[str] = None
    NOM3_RELA: Optional[str] = None
    NOM3_PER: Optional[str] = None
    NOM3_IDNO: Optional[str] = None
    NOM3_MIN_F: Optional[str] = None
    NOM3_DOB: Optional[str] = None
    NOM3_GUARD: Optional[str] = None
    NOM3_GRELA: Optional[str] = None
    NOM3_GPAN: Optional[str] = None
    NOM_COUNT: Optional[str] = None
    NOM_SOA: Optional[str] = None
    NOM1_ID_T: Optional[str] = None
    NOM2_ID_T: Optional[str] = None
    NOM3_ID_T: Optional[str] = None
    NOM1_EMAI: Optional[str] = None
    NOM2_EMAI: Optional[str] = None
    NOM3_EMAI: Optional[str] = None
    NOM1_MOB: Optional[str] = None
    NOM2_MOB: Optional[str] = None
    NOM3_MOB: Optional[str] = None
    NOM1_ADD1: Optional[str] = None
    NOM1_ADD2: Optional[str] = None
    NOM1_ADD3: Optional[str] = None
    NOM2_ADD1: Optional[str] = None
    NOM2_ADD2: Optional[str] = None
    NOM2_ADD3: Optional[str] = None
    NOM3_ADD1: Optional[str] = None
    NOM3_ADD2: Optional[str] = None
    NOM3_ADD3: Optional[str] = None
    NOM1_CITY: Optional[str] = None
    NOM1_PIN: Optional[str] = None
    NOM1_CON: Optional[str] = None
    NOM2_CITY: Optional[str] = None
    NOM2_PIN: Optional[str] = None
    NOM2_CON: Optional[str] = None
    NOM3_CITY: Optional[str] = None
    NOM3_PIN: Optional[str] = None
    NOM3_CON: Optional[str] = None


class NFTNOMRequest(BaseModel):
    nft_nominee_registration_modification_details: List[NFTNomItem]

    class Config:
        populate_by_name = True

    def to_nse_payload(self) -> dict:
        return {
            "nft_nominee_registration/modification_details": [
                item.model_dump(exclude_none=True)
                for item in self.nft_nominee_registration_modification_details
            ]
        }


class NFTNOMResponse(BaseModel):
    Message: Optional[str] = None
    Status: Optional[str] = None


class NFTCOAItem(BaseModel):
    AMC_CODE: Optional[str] = None
    FOLIO_NO: Optional[str] = None
    FH_NAME: Optional[str] = None
    TAX_NUMBER: Optional[str] = None
    DOC_TYPE: Optional[str] = None
    TWOFA_AUTH: Optional[str] = None
    IMG_REF_NO: Optional[str] = None
    EMAIL: Optional[str] = None
    MOBILE_NO: Optional[str] = None
    AB1_ACT_NO: Optional[str] = None
    AB1_HLD_NA: Optional[str] = None
    AB1_IFS_CD: Optional[str] = None
    AB1_ACT_TY: Optional[str] = None
    AB1_NAME: Optional[str] = None
    AB1_BR_NAM: Optional[str] = None
    AB2_ACT_NO: Optional[str] = None
    AB2_HLD_NA: Optional[str] = None
    AB2_IFS_CD: Optional[str] = None
    AB2_ACT_TY: Optional[str] = None
    AB2_NAME: Optional[str] = None
    AB2_BR_NAM: Optional[str] = None
    AB3_ACT_NO: Optional[str] = None
    AB3_HLD_NA: Optional[str] = None
    AB3_IFS_CD: Optional[str] = None
    AB3_ACT_TY: Optional[str] = None
    AB3_NAME: Optional[str] = None
    AB3_BR_NAM: Optional[str] = None
    AB4_ACT_NO: Optional[str] = None
    AB4_HLD_NA: Optional[str] = None
    AB4_IFS_CD: Optional[str] = None
    AB4_ACT_TY: Optional[str] = None
    AB4_NAME: Optional[str] = None
    AB4_BR_NAM: Optional[str] = None
    AB5_ACT_NO: Optional[str] = None
    AB5_HLD_NA: Optional[str] = None
    AB5_IFS_CD: Optional[str] = None
    AB5_ACT_TY: Optional[str] = None
    AB5_NAME: Optional[str] = None
    AB5_BR_NAM: Optional[str] = None


class NFTCOARequest(BaseModel):
    nft_change_of_bank_account_details: List[NFTCOAItem]

    def to_nse_payload(self) -> dict:
        return {
            "nft_change of bank_account_details": [
                item.model_dump(exclude_none=True)
                for item in self.nft_change_of_bank_account_details
            ]
        }


class NFTCODItem(BaseModel):
    AMC_CODE: Optional[str] = None
    FOLIO_NO: Optional[str] = None
    FH_NAME: Optional[str] = None
    TAX_NUMBER: Optional[str] = None
    DOC_TYPE: Optional[str] = None
    TWOFA_AUTH: Optional[str] = None
    IMG_REF_NO: Optional[str] = None
    EMAIL: Optional[str] = None
    MOBILE_NO: Optional[str] = None
    SCH_CODE: Optional[str] = None
    REINV_TAG: Optional[str] = None


class NFTCODRequest(BaseModel):
    nft_change_of_dividend_details: List[NFTCODItem]

    def to_nse_payload(self) -> dict:
        return {
            "nft_change of dividend_details": [
                item.model_dump(exclude_none=True)
                for item in self.nft_change_of_dividend_details
            ]
        }


class NFTCOBItem(BaseModel):
    AMC_CODE: Optional[str] = None
    FOLIO_NO: Optional[str] = None
    FH_NAME: Optional[str] = None
    TAX_NUMBER: Optional[str] = None
    DOC_TYPE: Optional[str] = None
    TWOFA_AUTH: Optional[str] = None
    IMG_REF_NO: Optional[str] = None
    EMAIL: Optional[str] = None
    MOBILE_NO: Optional[str] = None
    BROKE_CD: Optional[str] = None
    SBBR_CODE: Optional[str] = None
    EUIN: Optional[str] = None
    RIA_CODE: Optional[str] = None


class NFTCOBRequest(BaseModel):
    nft_change_of_broker_details: List[NFTCOBItem]

    def to_nse_payload(self) -> dict:
        return {
            "nft_change of broker_details": [
                item.model_dump(exclude_none=True)
                for item in self.nft_change_of_broker_details
            ]
        }


class NFTResponse(BaseModel):
    Message: Optional[str] = None
    Status: Optional[str] = None


class NFTCOCItem(BaseModel):
    AMC_CODE: Optional[str] = None
    FOLIO_NO: Optional[str] = None
    FH_NAME: Optional[str] = None
    TAX_NUMBER: Optional[str] = None
    DOC_TYPE: Optional[str] = None
    TWOFA_AUTH: Optional[str] = None
    IMG_REF_NO: Optional[str] = None
    EMAIL: Optional[str] = None
    MOBILE_NO: Optional[str] = None
    J1_EMAIL: Optional[str] = None
    J1_MOBILE: Optional[str] = None
    J2_EMAIL: Optional[str] = None
    J2_MOBILE: Optional[str] = None
    PH_EMA_DEC: Optional[str] = None
    PH_MOB_DEC: Optional[str] = None
    J1_EMA_DEC: Optional[str] = None
    J1_MOB_DEC: Optional[str] = None
    J2_EMA_DEC: Optional[str] = None
    J2_MOB_DEC: Optional[str] = None


class NFTCOCRequest(BaseModel):
    nft_change_of_contact_details: List[NFTCOCItem]

    def to_nse_payload(self) -> dict:
        return {
            "nft_change_of contact_details": [
                item.model_dump(exclude_none=True)
                for item in self.nft_change_of_contact_details
            ]
        }


class NFTCOFItem(BaseModel):
    AMC_CODE: Optional[str] = None
    FOLIO_NO: Optional[str] = None
    FH_NAME: Optional[str] = None
    TAX_NUMBER: Optional[str] = None
    DOC_TYPE: Optional[str] = None
    TWOFA_AUTH: Optional[str] = None
    IMG_REF_NO: Optional[str] = None
    EMAIL: Optional[str] = None
    MOBILE_NO: Optional[str] = None
    SRC_FOLIO: Optional[str] = None


class NFTCOFRequest(BaseModel):
    nft_consolidation_folio_details: List[NFTCOFItem]

    def to_nse_payload(self) -> dict:
        return {
            "nft_consolidation of folio_details": [
                item.model_dump(exclude_none=True)
                for item in self.nft_consolidation_folio_details
            ]
        }


class NFTCOMItem(BaseModel):
    AMC_CODE: Optional[str] = None
    FOLIO_NO: Optional[str] = None
    FH_NAME: Optional[str] = None
    TAX_NUMBER: Optional[str] = None
    DOC_TYPE: Optional[str] = None
    TWOFA_AUTH: Optional[str] = None
    IMG_REF_NO: Optional[str] = None
    EMAIL: Optional[str] = None
    MOBILE_NO: Optional[str] = None
    PB_ACT_NO: Optional[str] = None
    PB_HLD_NAM: Optional[str] = None
    PB_IFSC_CD: Optional[str] = None
    PB_ACT_TY: Optional[str] = None
    PB_NAM: Optional[str] = None
    PB_BR_NAM: Optional[str] = None


class NFTCOMRequest(BaseModel):
    nft_change_of_bank_account_details: List[NFTCOMItem]

    def to_nse_payload(self) -> dict:
        return {
            "nft_change of bank_account_details": [
                item.model_dump(exclude_none=True)
                for item in self.nft_change_of_bank_account_details
            ]
        }


class NFTImageUploadRequest(BaseModel):
    img_name: str
    img_data: str


class NFTImageUploadResponse(BaseModel):
    img_name: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None


class SIPModItem(BaseModel):
    sys_reg_no: Optional[str] = None
    primary_holder_email: Optional[str] = None
    primary_holder_mobile: Optional[str] = None
    sub_broker_code: Optional[str] = None
    sub_broker_arn: Optional[str] = None
    euin_number: Optional[str] = None
    folio_no: Optional[str] = None
    trans_mode: Optional[str] = None
    amount: Optional[Any] = None
    units: Optional[str] = None
    remarks: Optional[str] = None
    send_2fa: Optional[str] = None
    send_comm: Optional[str] = None
    filler_1: Optional[str] = None
    filler_2: Optional[str] = None
    member_unique_id: Optional[str] = None


class SIPModRequest(BaseModel):
    mod_data: List[SIPModItem]


class SIPModResponse(BaseModel):
    mod_data: Optional[List[Any]] = None


class KycFreshRegisterRequest(BaseModel):
    pan_no: str
    client_code: str
    mobile_no: Optional[str] = None
    email: Optional[str] = None
    filler_1: Optional[str] = None
    filler_2: Optional[str] = None


class KycFreshRegisterResponse(BaseModel):
    pan_no: Optional[str] = None
    client_code: Optional[str] = None
    status: Optional[str] = None
    remarks: Optional[str] = None
