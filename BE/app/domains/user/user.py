from typing import Optional


class User:
    """User represents your collection of books as an entity."""

    def __init__(
        self,
        id: str,
        name: str,
        address: str,
        telephone: str,
        avatar: str,
        work_for: int,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.id: str = id
        self.name: str = name
        self.address: str = address
        self.telephone: int = telephone
        self.avatar: str = avatar
        self.work_for: int = work_for
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

    def __eq__(self, o: object) -> bool:
        if isinstance(o, User):
            return self.id == o.id

        return False