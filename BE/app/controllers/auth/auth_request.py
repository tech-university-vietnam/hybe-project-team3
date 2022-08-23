from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str
    address: str
    email: str
    telephone: str
    avatar: str
    work_for: int


class LoginRequest(BaseModel):
    username: str
    email: str
    password: str
