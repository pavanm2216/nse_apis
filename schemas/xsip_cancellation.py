from pydantic import BaseModel
from typing import Optional, List


class XSIPCancellationDetail(BaseModel):
    client_code: Optional[str] = None
    xsip_reg_no: Optional[str] = None
    remarks: Optional[str] = None
    can_status: Optional[str] = None
    can_remark: Optional[str] = None


class XSIPCancellationRequest(BaseModel):
    can_data: List[XSIPCancellationDetail]


class XSIPCancellationResponse(BaseModel):
    reg_data: Optional[List[XSIPCancellationDetail]] = None

    model_config = {"extra": "allow"}
