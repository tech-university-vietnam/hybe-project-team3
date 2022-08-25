from typing import Optional

from app.controllers.auth.auth_request import RegisterRequest
from app.infrastructure.postgresql.database import session
from app.infrastructure.postgresql.user.user_dto import UserDTO
from app.model.user import User


class UserRepository:
    """User Repository defines a repository interface for user entity."""

    def create(self, regis: RegisterRequest) -> bool:
        user_dto = UserDTO.from_register_request(regis)
        session.add(user_dto)
        session.commit()

        return bool(user_dto.id)

    def update(self, user: User) -> Optional[User]:
        pass

    def delete_by_id(self, id: str):
        pass
