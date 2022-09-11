from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class Hospital(BaseModel):
    """Hospital represents your collection of books as an entity."""

    id: int
    name: str
    telephone: str
    address: str
    join_date: datetime





class HospitalItem:
    """Hospital represents your collection of books as an entity."""

    def __init__(self,
                 id: int,
                 name: str,
                 ):
        self.id: int = id
        self.name: str = name

    def __eq__(self, o: object) -> bool:
        if isinstance(o, HospitalItem):
            return self.id == o.id
        return False
