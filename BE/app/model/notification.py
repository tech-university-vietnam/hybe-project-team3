from datetime import datetime
from optparse import Option
from typing import Optional

from pydantic import BaseModel


class NotificationIdPayload(BaseModel):
    id: int


class Notification:
    id: Optional[int]
    sourcing_id: int
    sourcing_type: str
    sourcing_name: str

    from_hospital_id: Optional[int]
    to_hospital_id: Optional[int]

    created_at: Optional[datetime]


class BuyerSellerMap:
    sourcing_id: int
    sourcing_type: Optional[str]
    sourcing_name: str

    from_hospital_id: int
    to_hospital_id: int

    created_at: Optional[datetime]
