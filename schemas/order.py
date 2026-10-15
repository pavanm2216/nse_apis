from pydantic import BaseModel, field_validator
from typing import Optional, List


class OrderRequest(BaseModel):
    scheme_code: str
    trxn_type: str
    buy_sell_type: str
    client_code: str
    demat_physical: str
    order_amount: str
    kyc_flag: str
    euin_declaration: str
    order_ref_number: Optional[str] = None
    folio_no: Optional[str] = None
    remarks: Optional[str] = None
    sub_broker_code: Optional[str] = None
    euin_number: Optional[str] = None
    min_redemption_flag: Optional[str] = None
    dpc_flag: Optional[str] = None
    all_units: Optional[str] = None
    redemption_units: Optional[str] = None
    sub_broker_arn: Optional[str] = None
    bank_ref_no: Optional[str] = None
    account_no: Optional[str] = None
    mobile_no: Optional[str] = None
    email: Optional[str] = None
    mandate_id: Optional[str] = None
    filler1: Optional[str] = None
    trxn_order_id: Optional[str] = None
    trxn_status: Optional[str] = None
    trxn_remark: Optional[str] = None
    member_unique_id: Optional[str] = None

    @field_validator("scheme_code")
    @classmethod
    def scheme_code_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("scheme_code is required and cannot be empty")
        return v


class OrderResponse(BaseModel):
    order_ref_number: Optional[str] = None
    scheme_code: Optional[str] = None
    trxn_type: Optional[str] = None
    buy_sell_type: Optional[str] = None
    client_code: Optional[str] = None
    demat_physical: Optional[str] = None
    order_amount: Optional[str] = None
    folio_no: Optional[str] = None
    remarks: Optional[str] = None
    kyc_flag: Optional[str] = None
    sub_broker_code: Optional[str] = None
    euin_number: Optional[str] = None
    euin_declaration: Optional[str] = None
    min_redemption_flag: Optional[str] = None
    dpc_flag: Optional[str] = None
    all_units: Optional[str] = None
    redemption_units: Optional[str] = None
    sub_broker_arn: Optional[str] = None
    bank_ref_no: Optional[str] = None
    account_no: Optional[str] = None
    mobile_no: Optional[str] = None
    email: Optional[str] = None
    mandate_id: Optional[str] = None
    filler1: Optional[str] = None
    trxn_order_id: Optional[str] = None
    trxn_status: Optional[str] = None
    trxn_remark: Optional[str] = None
    member_unique_id: Optional[str] = None


class OrderEntryRequest(BaseModel):
    transaction_details: List[OrderRequest]


class OrderEntryResponse(BaseModel):
    transaction_details: Optional[List[OrderResponse]] = None

    model_config = {"extra": "allow"}
