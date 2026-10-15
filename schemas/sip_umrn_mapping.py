from pydantic import BaseModel
from typing import Optional


class SIPUMRNMappingRequest(BaseModel):
    sip_reg_id: str
    umrn: str
    remark: Optional[str] = None


class SIPUMRNMappingResponse(BaseModel):
    sip_reg_id: Optional[str] = None
    umrn: Optional[str] = None
    remark: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None
