from pydantic import BaseModel


class AOFImageUploadRequest(BaseModel):
    client_code: str
    file_name: str
    document_type: str
    file_data: str


class AOFImageUploadResponse(BaseModel):
    status: str
    message: str
