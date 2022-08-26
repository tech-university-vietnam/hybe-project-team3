from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    password: str
    work_for: int


class LoginRequest(BaseModel):
    email: str
    password: str


class LogoutRequest(BaseModel):
    email: str
