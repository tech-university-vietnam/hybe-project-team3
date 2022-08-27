import logging
from typing import Optional
from app.controllers.auth.auth_request import RegisterRequest
from app.infrastructure.postgresql.user.user_dto import UserDTO
from app.model.user import User
from sqlalchemy import update, exc, and_, select


class UserRepository:
    """User Repository defines a repository interface for user entity."""

    def create(self, regis: RegisterRequest, db) -> bool:
        try:
            user_dto = UserDTO.from_register_request(regis)
            db.add(user_dto)
            db.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return False

    def update(self, user: User) -> Optional[User]:
        pass

    def delete_by_id(self, id: str):
        pass

    def add_new_token(self, id: str, token, db) -> bool:
        statement = update(UserDTO).where(UserDTO.id == id).values(
            token=token)
        print(statement)
        try:
            db.execute(statement)
            db.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return False

    def delete_token(self, id: str, email: str, db) -> str:
        statement = update(UserDTO).where(
            and_(UserDTO.id == id, UserDTO.email == email)).values(
                token=None)
        logging.info(statement)
        try:
            db.execute(statement)
            db.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return False

    def check_token(self, user_id: str, token: str, db) -> bool:
        statement = select(UserDTO.token).where(UserDTO.id == user_id)
        try:
            result: tuple = db.execute(statement).fetchone()
            db.commit()
            if (result[0] == token):
                return True
            else:
                return False
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return False
