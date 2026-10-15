from pydantic import BaseModel
from typing import Optional, List, Any


class MandateStatusReportRequest(BaseModel):
    mandate_id: Optional[str] = None
    client_code: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    memberMandateIds: Optional[str] = None


class MandateStatusReportResponse(BaseModel):
    response_status: Optional[str] = None
    report_data_total: Optional[str] = None
    report_data: Optional[List[Any]] = None
    error_remark: Optional[str] = None
