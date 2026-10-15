from pydantic import BaseModel
from typing import Optional, List, Any


class RedemptionStatementRequest(BaseModel):
    from_date: str
    to_date: str
    order_ids: Optional[str] = None
    order_type: Optional[str] = None
    sub_order_type: Optional[str] = None
    client_code: Optional[str] = None
    transaction_type: Optional[str] = None
    order_status: Optional[str] = None
    settlement_type: Optional[str] = None
    member_unique_ids: Optional[str] = None


class AllotmentStatementRequest(BaseModel):
    from_date: str
    to_date: str
    order_ids: Optional[str] = None
    order_type: Optional[str] = None
    sub_order_type: Optional[str] = None
    client_code: Optional[str] = None
    transaction_type: Optional[str] = None
    order_status: Optional[str] = None
    settlement_type: Optional[str] = None
    date_type: Optional[str] = None
    member_unique_ids: Optional[str] = None


class StatementReportResponse(BaseModel):
    response_status: Optional[str] = None
    report_data_total: Optional[Any] = None
    report_data: Optional[List[Any]] = None
    error_remark: Optional[str] = None
