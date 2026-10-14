from pydantic import BaseModel
from typing import Optional, List, Any


class OrderStatusRequest(BaseModel):
    from_date: str
    to_date: str
    trans_type: str
    order_type: str
    sub_order_type: str
    client_code: Optional[str] = None
    order_status: Optional[str] = None
    settlement_type: Optional[str] = None
    order_ids: Optional[str] = None
    member_unique_ids: Optional[str] = None
    date_type: Optional[str] = None
    instalment_no: Optional[str] = None
    sip_reg_nos: Optional[str] = None


class OrderStatusResponse(BaseModel):
    response_status: str
    report_data_total: str
    report_data: Optional[List[Any]] = None
    error_remark: Optional[str] = None
