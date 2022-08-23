import bcrypt

from app.controllers.auth.auth_request import RegisterRequest
from app.domain.auth.auth_repository import AuthRepository
from app.domain.user.user_repository import UserRepository


class AuthService:
    auth_repo = AuthRepository()
    user_repo = UserRepository()

    @staticmethod
    def compare_hash(password: str, hash_pw: str):
        password = password.encode('utf-8')
        hash_pw = hash_pw.encode('utf-8')

        return bcrypt.checkpw(password, hash_pw)

    def login(self, username, email, password) -> bool:
        # Returns jwt token
        auth_user = self.auth_repo.query_auth_user(username, email)

        if auth_user:
            return self.compare_hash(password, auth_user.hash_password)
        else:
            return False

    def register(self, register_req: RegisterRequest) -> bool:
        success = self.user_repo.create(register_req)
        return success
