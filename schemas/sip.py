from pydantic import BaseModel
from typing import Optional, List


class SIPDetail(BaseModel):
    amc_code: Optional[str] = None
    sch_code: Optional[str] = None
    client_code: Optional[str] = None
    internal_ref_no: Optional[str] = None
    trans_mode: Optional[str] = None
    dp_txn_mode: Optional[str] = None
    start_date: Optional[str] = None
    frequency_type: Optional[str] = None
    frequency_allowed: Optional[str] = None
    installment_amount: Optional[str] = None
    status: Optional[str] = None
    member_code: Optional[str] = None
    folio_no: Optional[str] = None
    sip_remarks: Optional[str] = None
    installment_no: Optional[str] = None
    sip_mandate_id: Optional[str] = None
    sub_broker_code: Optional[str] = None
    euin_number: Optional[str] = None
    euin_declaration: Optional[str] = None
    dpc_flag: Optional[str] = None
    first_order_today: Optional[str] = None
    sub_broker_arn: Optional[str] = None
    end_date: Optional[str] = None
    primary_holder_mobile: Optional[str] = None
    primary_holder_email: Optional[str] = None
    step_up_required: Optional[str] = None
    step_up_start_date: Optional[str] = None
    step_up_end_date: Optional[str] = None
    step_up_frequency: Optional[str] = None
    step_up_amount: Optional[str] = None
    goal_based_sip: Optional[str] = None
    goal_type: Optional[str] = None
    goal_name: Optional[str] = None
    goal_amount: Optional[str] = None
    filler_1: Optional[str] = None
    filler_2: Optional[str] = None
    filler_3: Optional[str] = None
    filler_4: Optional[str] = None
    filler_5: Optional[str] = None
    reg_id: Optional[str] = None
    reg_status: Optional[str] = None
    reg_remark: Optional[str] = None
    member_unique_id: Optional[str] = None


class SIPRegistrationRequest(BaseModel):
    reg_data: List[SIPDetail]


class SIPRegistrationResponse(BaseModel):
    reg_data: List[SIPDetail]
