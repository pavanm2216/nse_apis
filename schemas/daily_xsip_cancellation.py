from pydantic import BaseModel
from typing import Optional, List


class DailyXSIPCancellationDetail(BaseModel):
    client_code: Optional[str] = None
    xsip_reg_no: Optional[str] = None
    xsip_cancel_date: Optional[str] = None
    remarks: Optional[str] = None
    can_status: Optional[str] = None
    can_remark: Optional[str] = None


class DailyXSIPCancellationRequest(BaseModel):
    can_data: List[DailyXSIPCancellationDetail]


class DailyXSIPCancellationResponse(BaseModel):
    reg_data: List[DailyXSIPCancellationDetail]
