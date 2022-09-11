import logging
from typing import Optional

from app.controllers.user.auth_request import RegisterRequest
from app.domains.helpers.database_repository import DatabaseRepository
from app.domains.user.user_exception import EmailAlreadyRegisteredError, EmailNotFoundError

from app.infrastructure.postgresql.user.user_dto import UserDTO
from app.infrastructure.postgresql.hospital.hospital import HospitalDTO
from app.model.user import User, SafeUser, DetailUser
from app.common.exceptions import DBError
from sqlalchemy import update, exc, and_, select


class UserRepository:
    """User Repository defines a repository interface for user entity."""

    def __init__(self, database_repository: DatabaseRepository):
        self.db_repo = database_repository
        self.db = next(self.db_repo.get_db())

    def create(self, regis: RegisterRequest) -> Optional[User]:
        try:
            user_dto = UserDTO.from_register_request(regis)
            self.db.add(user_dto)
            self.db.commit()
            return user_dto.to_entity()
        except exc.IntegrityError:
            raise EmailAlreadyRegisteredError
        except exc.SQLAlchemyError:
            raise DBError

    def get_by_id(self, id: str) -> Optional[SafeUser]:
        statement = select(UserDTO, HospitalDTO).join(HospitalDTO.users).where(
            UserDTO.id == id)
        try:
            user_dto = self.db.execute(statement).scalar_one()
            return user_dto.to_safe_entity()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return

    def get_detail_by_id(self, id: str) -> Optional[DetailUser]:
        statement = select(UserDTO, HospitalDTO).join(HospitalDTO.users).where(
            UserDTO.id == id)
        try:
            user_dto: UserDTO = self.db.execute(statement).scalar_one()
            return user_dto.to_detail_entity()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return

    def update(self, user: User) -> Optional[User]:
        pass

    def delete_by_id(self, id: str):
        pass

    def add_new_token(self, id: int, token) -> bool:
        statement = update(UserDTO).where(UserDTO.id == id).values(
            token=token)
        try:
            self.db.execute(statement)
            self.db.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return False

    def delete_token(self, id: str, email: str) -> bool:
        statement = update(UserDTO).where(
            and_(UserDTO.id == id, UserDTO.email == email)).values(
            token=None)
        logging.info(statement)
        try:
            self.db.execute(statement)
            self.db.commit()
            return True
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return False

    def check_token(self, user_id: str, token: str) -> bool:
        statement = select(UserDTO.token).where(UserDTO.id == user_id)
        try:
            user = self.db.execute(statement).first()
            if not user:
                return False

            if user[0] == token:
                return True
            else:
                return False
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return False

    def get_by_email(self, email: str) -> Optional[User]:
        # Query from database here
        user_dto = self.db.query(UserDTO).filter(
        (UserDTO.email == email)).first()
        if user_dto:
            return user_dto.to_entity()
        else:
            raise EmailNotFoundError
