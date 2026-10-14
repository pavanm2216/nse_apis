from pydantic import BaseModel


class MandateImageUploadRequest(BaseModel):
    client_code: str
    mandate_id: str
    file_name: str
    file_data: str


class MandateImageUploadResponse(BaseModel):
    status: str
    message: str
