from pydantic import BaseModel
from typing import Optional, List, Any


class SecuritiesDeliveryRequest(BaseModel):
    from_date: str
    to_date: str
    date_type: Optional[str] = None
    client_code: Optional[str] = None
    settlement_type: Optional[str] = None
    dp_type: Optional[str] = None
    order_ids: Optional[str] = None
    member_unique_ids: Optional[str] = None


class TwoFAReportRequest(BaseModel):
    from_date: str
    to_date: str
    product_type: Optional[str] = None
    product_id: Optional[str] = None
    client_code: Optional[str] = None


class ClientAuthorizationRequest(BaseModel):
    from_date: str
    to_date: str
    client_code: Optional[str] = None
    auth_status: Optional[str] = None
    date_type: Optional[str] = None


class ClientDetailReportRequest(BaseModel):
    from_date: str
    to_date: str
    client_code: Optional[str] = None
    auth_status: Optional[str] = None
    date_type: Optional[str] = None


class OrderLifecycleRequest(BaseModel):
    from_date: str
    to_date: str
    Product_type: Optional[str] = None
    product_id: Optional[str] = None
    client_code: Optional[str] = None


class TransactionDetailRequest(BaseModel):
    from_date: str
    to_date: str
    client_code: Optional[str] = None
    applicant_name: Optional[str] = None
    pan: Optional[str] = None
    order_id: Optional[str] = None
    systematic_reg_id: Optional[str] = None
    date_type: Optional[str] = None


class FATCAReportRequest(BaseModel):
    pan_pkern_no: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class AOFImageUploadReportRequest(BaseModel):
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class ELOGUploadReportRequest(BaseModel):
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class SIPRegReportRequest(BaseModel):
    sip_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    member_unique_ids: Optional[str] = None


class SIPCanReportRequest(BaseModel):
    sip_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class SIPInstDueReportRequest(BaseModel):
    sip_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class SIPTopupReportRequest(BaseModel):
    parent_sip_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class StepupRegReportRequest(BaseModel):
    sip_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class XSIPRegReportRequest(BaseModel):
    xsip_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    member_unique_ids: Optional[str] = None


class XSIPCanReportRequest(BaseModel):
    xsip_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class XSIPInstDueReportRequest(BaseModel):
    xsip_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class XSIPTopupReportRequest(BaseModel):
    parent_xsip_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class STPRegReportRequest(BaseModel):
    stp_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    member_unique_ids: Optional[str] = None


class STPCanReportRequest(BaseModel):
    stp_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class STPInstDueReportRequest(BaseModel):
    stp_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class SWPRegReportRequest(BaseModel):
    swp_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    member_unique_ids: Optional[str] = None


class SWPCanReportRequest(BaseModel):
    swp_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class SWPInstDueReportRequest(BaseModel):
    swp_reg_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class MasterDownloadRequest(BaseModel):
    file_type: str


class ClientKYCReportRequest(BaseModel):
    pan_no: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


class GenericReportResponse(BaseModel):
    response_status: Optional[str] = None
    report_data_total: Optional[str] = None
    response_data_total: Optional[str] = None
    report_data: Optional[List[Any]] = None
    error_remark: Optional[str] = None
