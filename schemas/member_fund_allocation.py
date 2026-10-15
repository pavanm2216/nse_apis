from pydantic import BaseModel, field_validator
from typing import Optional, List, Any
import re

DD_MM_YYYY = re.compile(r"^\d{2}-\d{2}-\d{4}$")


class MemberFundOrderWiseRequest(BaseModel):
    from_date: str  # must be dd-MM-yyyy
    to_date: str    # must be dd-MM-yyyy
    client_code: Optional[str] = None
    pg_bank_refno: Optional[str] = None
    order_id: Optional[str] = None
    pg_agencyid: Optional[str] = None

    @field_validator("from_date", "to_date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        if not DD_MM_YYYY.match(v):
            raise ValueError("Date must be in dd-MM-yyyy format (e.g. 01-09-2026)")
        return v


class MemberFundAgeWiseRequest(BaseModel):
    date: str
    client_code: Optional[str] = None
    settlement_type: Optional[str] = None
    amc_code: Optional[str] = None
    scheme_code: Optional[str] = None


class MemberFundAllocationResponse(BaseModel):
    response_status: Optional[str] = None
    report_data_total: Optional[Any] = None
    report_data: Optional[List[Any]] = None
    error_remark: Optional[str] = None
