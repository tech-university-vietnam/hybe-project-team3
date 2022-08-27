from typing import Optional
from app.domain.user.user_repository import UserRepository

from app.controllers.auth.auth_request import RegisterRequest
from app.model.user import User


class UserService:
    """User service defines a repository interface for user entity."""
    user_repo = UserRepository()

    def create(self, regis: RegisterRequest, db) -> bool:
        user_dto = self.user_repo.create(regis, db)
        return bool(user_dto.id)

    def update(self, user: User) -> Optional[User]:
        pass

    def delete_by_id(self, id: str):
        pass

    def add_new_token(self, id: str, token: str, db) -> bool:
        return self.user_repo.add_new_token(id, token, db)

    def delete_token(self, user_id: str, email: str, db) -> bool:
        return self.user_repo.delete_token(user_id, email, db)
