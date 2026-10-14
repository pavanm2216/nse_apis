from pydantic import BaseModel
from typing import Optional, List, Any


class MemberFundOrderWiseRequest(BaseModel):
    from_date: str
    to_date: str
    client_code: Optional[str] = None
    pg_bank_refno: Optional[str] = None
    order_id: Optional[str] = None
    pg_agencyid: Optional[str] = None


class MemberFundAgeWiseRequest(BaseModel):
    date: str
    client_code: Optional[str] = None
    settlement_type: Optional[str] = None
    amc_code: Optional[str] = None
    scheme_code: Optional[str] = None


class MemberFundAllocationResponse(BaseModel):
    response_status: str
    report_data_total: str
    report_data: Optional[List[Any]] = None
    error_remark: Optional[str] = None
