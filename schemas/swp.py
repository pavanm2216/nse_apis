from pydantic import BaseModel
from typing import Optional, List


class SWPDetail(BaseModel):
    client_code: Optional[str] = None
    scheme_code: Optional[str] = None
    trans_mode: Optional[str] = None
    folio_no: Optional[str] = None
    internal_ref_no: Optional[str] = None
    start_date: Optional[str] = None
    frequency_type: Optional[str] = None
    no_of_withdrawals: Optional[str] = None
    end_date: Optional[str] = None
    installment_amount: Optional[str] = None
    installment_units: Optional[str] = None
    first_order_today: Optional[str] = None
    sub_broker_code: Optional[str] = None
    euin_declaration: Optional[str] = None
    euin_number: Optional[str] = None
    remarks: Optional[str] = None
    sub_broker_arn: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    account_no: Optional[str] = None
    reg_id: Optional[str] = None
    reg_status: Optional[str] = None
    reg_remark: Optional[str] = None
    member_unique_id: Optional[str] = None


class SWPRegistrationRequest(BaseModel):
    reg_data: List[SWPDetail]


class SWPRegistrationResponse(BaseModel):
    reg_data: Optional[List[SWPDetail]] = None

    model_config = {"extra": "allow"}
