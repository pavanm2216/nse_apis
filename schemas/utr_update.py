from pydantic import BaseModel
from typing import Optional, List


class UTRDetail(BaseModel):
    client_code: Optional[str] = None
    bank_name: Optional[str] = None
    account_no: Optional[str] = None
    ifsc: Optional[str] = None
    utr_no: Optional[str] = None
    transfer_date: Optional[str] = None
    order_id: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None


class UTRUpdateRequest(BaseModel):
    utr_details: List[UTRDetail]


class UTRUpdateResponse(BaseModel):
    utr_details: List[UTRDetail]
