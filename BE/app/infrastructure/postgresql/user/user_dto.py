from datetime import datetime
from typing import Union

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import func
from app.controllers.auth.auth_request import RegisterRequest
from app.infrastructure.postgresql.database import Base
from app.model.user import User
import bcrypt
from datetime import datetime

class UserDTO(Base):
    """userDTO is a data transfer object associated with User entity."""

    __tablename__ = "User"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)

    # Login method
    username: Union[str, Column] = Column(String, nullable=False)
    email: Union[str, Column] = Column(String, nullable=False)
    telephone: Union[str, Column] = Column(String, nullable=False)
    # Auth data
    hash_pw: Union[str, Column] = Column(String, nullable=False)

    # Additional info
    address: Union[str, Column] = Column(String, nullable=False)
    avatar: Union[str, Column] = Column(String, nullable=False)
    # created_at: Union[datetime, Column] = Column(DateTime(timezone=True), server_default=func.now())

    created_at: Union[datetime, Column] = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at: Union[datetime, Column] = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Foreign key, Todo: Remove mock
    # hospital_id: Union[int, Column] = Column()
    hospital_id = 1
    work_for: Union[int, Column] = Column(Integer, nullable=False)

    def to_entity(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            email=self.email,
            address=self.address,
            telephone=self.telephone,
            avatar=self.avatar,
            work_for=self.hospital_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(user: User) -> "UserDTO":
        now = datetime.now()
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            address=user.address,
            telephone=user.telephone,
            avatar=user.avatar,
            work_for=user.work_for,
            created_at=now,
            updated_at=now,
        )

    @staticmethod
    def from_register_request(regis_req: RegisterRequest) -> "UserDTO":
        salt = bcrypt.gensalt()
        password = regis_req.password.encode('utf8')
        pwhash = bcrypt.hashpw(password, salt).decode('utf8')
        now = datetime.now()
        return UserDTO(
            username=regis_req.username,
            hash_pw=pwhash,
            email=regis_req.email,
            address=regis_req.address,
            telephone=regis_req.telephone,
            avatar=regis_req.avatar,
            work_for=regis_req.work_for,
            created_at = now,
            updated_at = now
        )
