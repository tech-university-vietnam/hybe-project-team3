from typing import Optional
from app.domains.user.user_repository import UserRepository

from app.controllers.user.auth_request import RegisterRequest
from app.model.user import User


class UserService:
    """User service defines a repository interface for user entity."""

    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    def create(self, regis: RegisterRequest) -> bool:
        user_dto = self.user_repo.create(regis)
        return user_dto and bool(user_dto.id)

    def update(self, user: User) -> Optional[User]:
        pass

    def delete_by_id(self, id: str):
        pass

    def add_new_token(self, id: int, token: str) -> bool:
        return self.user_repo.add_new_token(id, token)

    def delete_token(self, user_id: str, email: str) -> bool:
        return self.user_repo.delete_token(user_id, email)
