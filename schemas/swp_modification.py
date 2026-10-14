from pydantic import BaseModel
from typing import Optional, List


class SWPModDetail(BaseModel):
    sys_reg_no: Optional[str] = None
    primary_holder_email: Optional[str] = None
    primary_holder_mobile: Optional[str] = None
    sub_broker_code: Optional[str] = None
    sub_broker_arn: Optional[str] = None
    euin_number: Optional[str] = None
    folio_no: Optional[str] = None
    trans_mode: Optional[str] = None
    amount: Optional[str] = None
    remarks: Optional[str] = None
    send_2fa: Optional[str] = None
    send_comm: Optional[str] = None
    filler_1: Optional[str] = None
    filler_2: Optional[str] = None
    member_unique_id: Optional[str] = None
    status: Optional[str] = None
    status_remarks: Optional[str] = None


class SWPModificationRequest(BaseModel):
    mod_data: List[SWPModDetail]


class SWPModificationResponse(BaseModel):
    mod_data: List[SWPModDetail]
