from pydantic import BaseModel
from typing import Optional, List


class STPDetail(BaseModel):
    client_code: Optional[str] = None
    from_scheme_code: Optional[str] = None
    to_scheme_code: Optional[str] = None
    buy_sell_type: Optional[str] = None
    transaction_mode: Optional[str] = None
    folio_no: Optional[str] = None
    internal_ref_number: Optional[str] = None
    start_date: Optional[str] = None
    frequency_type: Optional[str] = None
    no_of_transfers: Optional[str] = None
    to_date: Optional[str] = None
    installment_amount: Optional[str] = None
    installment_units: Optional[str] = None
    first_order_today: Optional[str] = None
    sub_broker_code: Optional[str] = None
    euin_declaration: Optional[str] = None
    euin_number: Optional[str] = None
    remarks: Optional[str] = None
    sub_broker_arn_code: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    reg_id: Optional[str] = None
    reg_status: Optional[str] = None
    reg_remark: Optional[str] = None
    member_unique_id: Optional[str] = None


class STPRegistrationRequest(BaseModel):
    reg_data: List[STPDetail]


class STPRegistrationResponse(BaseModel):
    reg_data: List[STPDetail]
