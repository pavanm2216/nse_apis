from pydantic import BaseModel
from typing import Optional, List


class ClientBankDetailItem(BaseModel):
    client_code: Optional[str] = None
    action_type: Optional[str] = None
    account_type: Optional[str] = None
    account_no: Optional[str] = None
    micr_no: Optional[str] = None
    ifsc_code: Optional[str] = None
    default_bank_flag: Optional[str] = None
    status: Optional[str] = None
    error_remark: Optional[str] = None


class ClientBankDetailRequest(BaseModel):
    bank_dtl: List[ClientBankDetailItem]


class ClientBankDetailResponse(BaseModel):
    bank_dtl: List[ClientBankDetailItem]
