from pydantic import BaseModel


class CancelChequeUploadRequest(BaseModel):
    file_name: str
    client_code: str
    account_no: str
    ifsc: str
    account_type: str
    file_data: str


class CancelChequeUploadResponse(BaseModel):
    status: str
    message: str
