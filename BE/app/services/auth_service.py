from typing import Optional
import bcrypt

from fastapi import HTTPException
from app.controllers.user.auth_request import RegisterRequest
from app.domains.user.user_repository import UserRepository

from app.model.auth import Auth


class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    @staticmethod
    def compare_hash(password: str, hash_pw: str):
        password = password.encode('utf8')
        hash_pw = hash_pw.encode('utf8')

        return bcrypt.checkpw(password, hash_pw)

    def login(self, email, password) -> Optional[Auth]:
        # Returns jwt token
        user = self.user_repo.get_by_email(email)

        auth = Auth.from_user(user)

        if auth and self.compare_hash(password, auth.hash_pw):
            return auth
        else:
            raise HTTPException(status_code=404,
                                detail="Wrong email or password")

    def register(self, register_req: RegisterRequest) -> bool:
        return self.user_repo.create(register_req)
