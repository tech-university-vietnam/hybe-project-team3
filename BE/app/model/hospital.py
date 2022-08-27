from typing import Optional
from datetime import datetime


class Hospital:
    """Hospital represents your collection of books as an entity."""

    def __init__(self,
                 id: int,
                 name: str,
                 telephone: str,
                 address: str,
                 join_date: Optional[datetime] = datetime.now(),
                 ):
        self.id: int = id
        self.name: str = name
        self.telephone: str = telephone
        self.address: str = address
        self.join_date: datetime = join_date

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Hospital):
            return self.id == o.id
        return False


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