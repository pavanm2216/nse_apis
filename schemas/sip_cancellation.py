from pydantic import BaseModel
from typing import Optional, List


class SIPCancellationDetail(BaseModel):
    client_code: Optional[str] = None
    sip_reg_no: Optional[str] = None
    remarks: Optional[str] = None
    can_status: Optional[str] = None
    can_remark: Optional[str] = None


class SIPCancellationRequest(BaseModel):
    can_data: List[SIPCancellationDetail]


class SIPCancellationResponse(BaseModel):
    reg_data: Optional[List[SIPCancellationDetail]] = None

    model_config = {"extra": "allow"}
