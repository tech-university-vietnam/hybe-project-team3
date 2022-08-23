from typing import Optional
from datetime import datetime


class User:
    """User represents your collection of books as an entity."""

    def __init__(self,
                 id: str,
                 username: str,
                 email: str,
                 address: str,
                 telephone: str,
                 avatar: str,
                 work_for: int,
                 created_at: Optional[datetime] = datetime.now(),
                 updated_at: Optional[datetime] = datetime.now(),
                 ):
        self.id: Optional[str] = id
        self.username: str = username
        self.email: str = email
        self.address: str = address
        self.telephone: str = telephone
        self.avatar: str = avatar
        self.work_for: int = work_for
        self.created_at = created_at
        self.updated_at = updated_at

    def __eq__(self, o: object) -> bool:
        if isinstance(o, User):
            return self.id == o.id

        return False

