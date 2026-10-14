from pydantic import BaseModel
from typing import Optional, List


class SIPAmcPauseDetail(BaseModel):
    client_code: Optional[str] = None
    reg_type: Optional[str] = None
    sip_reg_no: Optional[str] = None
    modification_type: Optional[str] = None
    no_of_installments: Optional[str] = None
    pause_from: Optional[str] = None
    filler_1: Optional[str] = None
    filler_2: Optional[str] = None
    filler_3: Optional[str] = None
    filler_4: Optional[str] = None
    nse_remarks: Optional[str] = None
    status_flag: Optional[str] = None
    request_id: Optional[str] = None


class SIPAmcPauseRequest(BaseModel):
    pause_data: List[SIPAmcPauseDetail]


class SIPAmcPauseResponse(BaseModel):
    pause_data: List[SIPAmcPauseDetail]


class SIPAmcPauseReportRequest(BaseModel):
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    client_code: Optional[str] = None
    registration_no: Optional[str] = None
    modification_type: Optional[str] = None
    request_id: Optional[str] = None


class SIPAmcPauseReportResponse(BaseModel):
    response_status: Optional[str] = None
    response_data_total: Optional[str] = None
    report_data: Optional[List[dict]] = None
    error_remark: Optional[str] = None
