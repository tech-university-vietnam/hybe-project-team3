from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TrackingMedicine(BaseModel):
    id: int
    name: str
    number: Optional[int]
    status: str

    expired_date: datetime
