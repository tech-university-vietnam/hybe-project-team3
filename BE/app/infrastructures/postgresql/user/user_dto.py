from datetime import datetime
from typing import Union

from sqlalchemy import Column, String, DateTime
from BE.app.domains.user.user import User
from BE.app.infrastructures.postgresql.database import Base

def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class UserDTO(Base):
    """userDTO is a data transfer object associated with User entity."""

    __tablename__ = "User"
    id: Union[str, Column] = Column(String, primary_key=True, autoincrement=False)
    name: Union[str, Column] = Column(String, nullable=False)
    address: Union[str, Column] = Column(String, nullable=False)
    telephone: Union[str, Column] = Column(String, nullable=False)
    avatar: Union[str, Column] = Column(String, nullable=False)
    created_at: Union[datetime, Column] = Column(DateTime, index=True, nullable=False)
    updated_at: Union[datetime, Column] = Column(DateTime, index=True, nullable=False)

    def to_entity(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            address=self.address,
            telephone= self.telephone,
            avatar= self.avatar,
            work_for = self.avatar,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(user: User) -> "UserDTO":
        now = unixtimestamp()
        return UserDTO(
            id=user.id,
            name=user.name,
            address=user.address,
            telephone=user.telephone,
            avatar=user.avatar,
            work_for=user.work_for,
            created_at=now,
            updated_at=now,
        )