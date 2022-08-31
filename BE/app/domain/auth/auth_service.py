from typing import Optional
import bcrypt

from fastapi import HTTPException
from app.controllers.auth.auth_request import RegisterRequest
from app.domain.auth.auth_repository import AuthRepository
from app.domain.user.user_repository import UserRepository

from app.model.auth import Auth


class AuthService:

    def __init__(self, auth_repository: AuthRepository, user_repository: UserRepository):
        self.auth_repo = auth_repository
        self.user_repo = user_repository

    @staticmethod
    def compare_hash(password: str, hash_pw: str):
        password = password.encode('utf8')
        hash_pw = hash_pw.encode('utf8')

        return bcrypt.checkpw(password, hash_pw)

    def login(self, email, password) -> Optional[Auth]:
        # Returns jwt token
        auth_user = self.auth_repo.query_auth_user(email)

        if auth_user and self.compare_hash(password, auth_user.hash_pw):
            return auth_user
        else:
            raise HTTPException(status_code=404,
                                detail="Wrong email or password")

    def register(self, register_req: RegisterRequest) -> bool:
        return self.user_repo.create(register_req)
