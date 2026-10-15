from pydantic import BaseModel
from typing import Optional, List


class SwitchDetail(BaseModel):
    order_ref_number: Optional[str] = None
    from_scheme_code: Optional[str] = None
    to_scheme_code: Optional[str] = None
    buy_sell_type: Optional[str] = None
    client_code: Optional[str] = None
    demat_physical: Optional[str] = None
    amount: Optional[str] = None
    units: Optional[str] = None
    all_units: Optional[str] = None
    folio_no: Optional[str] = None
    remarks: Optional[str] = None
    kyc_flag: Optional[str] = None
    sub_broker_code: Optional[str] = None
    euin_number: Optional[str] = None
    euin_declaration: Optional[str] = None
    sub_broker_arn: Optional[str] = None
    mobile_no: Optional[str] = None
    email: Optional[str] = None
    filler1: Optional[str] = None
    filler2: Optional[str] = None
    filler3: Optional[str] = None
    trxn_so_order_id: Optional[str] = None
    trxn_si_order_id: Optional[str] = None
    trxn_status: Optional[str] = None
    trxn_remark: Optional[str] = None
    member_unique_id: Optional[str] = None


class SwitchEntryRequest(BaseModel):
    transaction_details: List[SwitchDetail]


class SwitchEntryResponse(BaseModel):
    transaction_details: Optional[List[SwitchDetail]] = None

    model_config = {"extra": "allow"}
