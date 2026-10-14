from pydantic import BaseModel


class POAUploadRequest(BaseModel):
    client_code: str
    file_name: str
    file_data: str


class POAUploadResponse(BaseModel):
    status: str
    message: str
