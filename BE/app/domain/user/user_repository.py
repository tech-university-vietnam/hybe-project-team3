import logging
from typing import Optional

from app.controllers.auth.auth_request import RegisterRequest
from app.infrastructure.postgresql.database import session
from app.infrastructure.postgresql.user.user_dto import UserDTO
from app.model.user import User
from sqlalchemy import update, exc, and_


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

    def add_new_token(self, id: str, token) -> bool:
        statement = update(UserDTO).where(UserDTO.id == id).values(
            token=token)
        try:
            session.execute(statement)
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return False

    def delete_token(self, id: str, email: str) -> str:
        statement = update(UserDTO).where(
            and_(UserDTO.id == id, UserDTO.email == email)).values(
                token=None)
        try:
            session.execute(statement)
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return False
