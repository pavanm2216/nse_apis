from pydantic import BaseModel
from typing import Optional, List


class STPCancellationDetail(BaseModel):
    client_code: Optional[str] = None
    stp_reg_no: Optional[str] = None
    remarks: Optional[str] = None
    can_status: Optional[str] = None
    can_remark: Optional[str] = None


class STPCancellationRequest(BaseModel):
    can_data: List[STPCancellationDetail]


class STPCancellationResponse(BaseModel):
    reg_data: Optional[List[STPCancellationDetail]] = None

    model_config = {"extra": "allow"}
