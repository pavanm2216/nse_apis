from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    status: Optional[str] = None
    message: Optional[str] = None
    error_type: Optional[str] = None
