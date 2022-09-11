from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NotificationIdPayload(BaseModel):
    id: int


class SeenStatus:
    not_seen = 'not seen'
    seen = 'seen'


class Status:
    approved = 'approved'
    declined = 'declined'

    @classmethod
    def all(cls):
        return [cls.approved, cls.declined]


class Notification(BaseModel):
    id: int
    souring_id: Optional[int]
    sourcing_type: str
    sourcing_name: str

    status: str
    seen_status: str
    description: str

    from_hospital_id: Optional[int]
    to_hospital_id: Optional[int]

    created_at: datetime
