from pydantic import BaseModel
from typing import Optional, List


class MandateDetail(BaseModel):
    client_code: Optional[str] = None
    amount: Optional[str] = None
    mandate_type: Optional[str] = None
    account_no: Optional[str] = None
    ac_type: Optional[str] = None
    ifsc_code: Optional[str] = None
    micr_no: Optional[str] = None
    micr_code: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    registration_date: Optional[str] = None
    member_mandate_no: Optional[str] = None
    reg_id: Optional[str] = None
    reg_status: Optional[str] = None
    reg_remark: Optional[str] = None


class MandateRegistrationRequest(BaseModel):
    reg_data: List[MandateDetail]


class MandateRegistrationResponse(BaseModel):
    reg_data: List[MandateDetail]
