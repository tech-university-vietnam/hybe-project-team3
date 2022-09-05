from datetime import datetime
from typing import Union

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.model.user import SafeUser
from app.controllers.user.auth_request import RegisterRequest
from app.infrastructure.postgresql.database import Base
from app.infrastructure.postgresql.source_order_request.source_order_request import SourceOrderRequestDTO
from app.model.user import User
import bcrypt


class UserDTO(Base):
    """userDTO is a data transfer object associated with User entity."""

    __tablename__ = "user"
    id: Union[int, Column] = Column(Integer, primary_key=True,
                                    autoincrement=True)

    # Login method
    username: Union[str, Column] = Column(String, nullable=True)
    email: Union[str, Column] = Column(String, nullable=False, unique=True)
    telephone: Union[str, Column] = Column(String, nullable=True)
    # Auth data
    hash_pw: Union[str, Column] = Column(String, nullable=False)

    # Additional info
    avatar: Union[str, Column] = Column(String, nullable=True)
    # created_at: Union[datetime, Column] = Column(DateTime(timezone=True),
    #           server_default=func.now())

    created_at: Union[datetime, Column] = Column(DateTime(timezone=True),
                                                 nullable=True)
    updated_at: Union[datetime, Column] = Column(DateTime(timezone=True),
                                                 nullable=True)
    # jwt token
    token: Union[str, Column] = Column(String, nullable=True)
    token_created_at: Union[str, Column] = Column(String, nullable=True)
    work_for: Union[int, Column] = Column(Integer, ForeignKey("hospital.id"))
    source_order_request = relationship("SourceOrderRequestDTO",
                                        backref="user")

    def to_entity(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            email=self.email,
            hash_pw=self.hash_pw,
            token=self.token,
            telephone=self.telephone,
            avatar=self.avatar,
            work_for=self.work_for,
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
            telephone=user.telephone,
            avatar=user.avatar,
            work_for=user.work_for,
            created_at=now,
            updated_at=now,
        )

    def to_safe_entity(self) -> SafeUser:
        return SafeUser(
            id=self.id,
            username=self.username,
            email=self.email,
            work_for=self.hospital.id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_register_request(regis_req: RegisterRequest) -> "UserDTO":
        salt = bcrypt.gensalt()
        password = regis_req.password.encode('utf8')
        pwhash = bcrypt.hashpw(password, salt).decode('utf8')
        now = datetime.now()
        return UserDTO(
            hash_pw=pwhash,
            email=regis_req.email,
            work_for=regis_req.work_for,
            created_at=now,
            updated_at=now
        )
