from pydantic import BaseModel
from typing import Optional, List, Any
from enum import Enum


class RedemptionReportType(str, Enum):
    order_date = "Order Date"
    payout_date = "Payout Date"
    fund_transfer_date = "Fund Transfer Date"


class RedemptionPayoutRequest(BaseModel):
    report_type: RedemptionReportType
    from_date: str   # DD-MM-YYYY
    to_date: str     # DD-MM-YYYY, max 30 days gap
    amc_code: Optional[str] = None
    order_id: Optional[str] = None
    member_unique_ids: Optional[str] = None


class RedemptionPayoutResponse(BaseModel):
    response_status: Optional[str] = None
    report_data_total: Optional[str] = None
    report_data: Optional[List[Any]] = None
    error_remark: Optional[str] = None
