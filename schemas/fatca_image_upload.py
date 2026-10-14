from pydantic import BaseModel


class FATCAImageUploadRequest(BaseModel):
    file_name: str
    pan_no: str
    file_data: str


class FATCAImageUploadResponse(BaseModel):
    status: str
    message: str
