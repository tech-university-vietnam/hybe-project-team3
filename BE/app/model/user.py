from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel


class User:
    """User represents your collection of books as an entity."""

    def __init__(self,
                 id: int,
                 username: str,
                 email: str,
                 hash_pw: str,
                 token: str,
                 telephone: str,
                 avatar: str,
                 work_for: int,
                 created_at: Optional[datetime] = datetime.utcnow(),
                 updated_at: Optional[datetime] = datetime.utcnow(),
                 ):
        self.id: int = id
        self.username: str = username
        self.email: str = email
        self.hash_pw: str = hash_pw
        self.token: str = token
        self.telephone: str = telephone
        self.avatar: str = avatar
        self.work_for: int = work_for
        self.created_at = created_at
        self.updated_at = updated_at

    def __eq__(self, o: object) -> bool:
        if isinstance(o, User):
            return self.id == o.id
        return False


class SafeUser(BaseModel):
    """Safe User hide sensitive information as an entity."""
    id: int
    username: Optional[str]
    email: str
    work_for: str
    created_at: datetime
    updated_at: datetime


class DetailUser(SafeUser):
    pass
