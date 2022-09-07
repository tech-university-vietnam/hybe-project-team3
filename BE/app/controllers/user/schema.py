from datetime import datetime
from pydantic import BaseModel


class LoginResponse(BaseModel):
    token: str


class GetUserResponse(BaseModel):
    username: str
    email: str
    work_for: str
    created_at: datetime
    updated_at: datetime
