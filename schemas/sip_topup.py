from pydantic import BaseModel
from typing import Optional, List, Any


class SIPTopupDetail(BaseModel):
    client_code: Optional[str] = None
    req_type: Optional[str] = None
    sip_reg_no: Optional[Any] = None
    installment_amount: Optional[Any] = None
    topup_frequency: Optional[str] = None
    topup_amount: Optional[Any] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    internal_ref_no: Optional[str] = None
    primary_holder_mobile: Optional[str] = None
    primary_holder_email: Optional[str] = None
    reg_id: Optional[str] = None
    reg_status: Optional[str] = None
    reg_remark: Optional[str] = None


class SIPTopupRequest(BaseModel):
    reg_data: List[SIPTopupDetail]


class SIPTopupResponse(BaseModel):
    reg_data: List[SIPTopupDetail]
