from pydantic import BaseModel
from typing import Optional, List, Any


class RedemptionPayoutRequest(BaseModel):
    report_type: str
    from_date: str
    to_date: str
    amc_code: Optional[str] = None
    order_id: Optional[str] = None
    member_unique_ids: Optional[str] = None


class RedemptionPayoutResponse(BaseModel):
    response_status: str
    report_data_total: str
    report_data: Optional[List[Any]] = None
    error_remark: Optional[str] = None
