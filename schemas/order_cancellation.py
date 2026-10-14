from pydantic import BaseModel
from typing import Optional, List


class OrderCancellationDetail(BaseModel):
    client_code: Optional[str] = None
    order_no: Optional[str] = None
    remarks: Optional[str] = None
    can_status: Optional[str] = None
    can_remark: Optional[str] = None


class OrderCancellationRequest(BaseModel):
    can_data: List[OrderCancellationDetail]


class OrderCancellationResponse(BaseModel):
    reg_data: List[OrderCancellationDetail]
