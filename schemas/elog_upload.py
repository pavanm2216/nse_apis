from pydantic import BaseModel
from typing import Optional


class ELOGUploadRequest(BaseModel):
    client_code: str
    primary_holder_pan: str
    primary_holder_ip_address: str
    primary_holder_log_date: str
    second_holder_pan: Optional[str] = None
    second_holder_ip_address: Optional[str] = None
    second_holder_log_date: Optional[str] = None
    third_holder_pan: Optional[str] = None
    third_holder_ip_address: Optional[str] = None
    third_holder_log_date: Optional[str] = None


class ELOGUploadResponse(BaseModel):
    client_code: Optional[str] = None
    primary_holder_pan: Optional[str] = None
    primary_holder_ip_address: Optional[str] = None
    primary_holder_log_date: Optional[str] = None
    second_holder_pan: Optional[str] = None
    second_holder_ip_address: Optional[str] = None
    second_holder_log_date: Optional[str] = None
    third_holder_pan: Optional[str] = None
    third_holder_ip_address: Optional[str] = None
    third_holder_log_date: Optional[str] = None
    elog_status: Optional[str] = None
    elog_status_message: Optional[str] = None
