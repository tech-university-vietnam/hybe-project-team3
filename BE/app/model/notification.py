from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.model.hospital import Hospital


class NotificationIdPayload(BaseModel):
    id: int


class SeenStatus:
    not_seen = 'not seen'
    seen = 'seen'


class Type:
    warning_expired = 'warningExpired'
    notify_sold = 'notifySold'
    notify_available = 'notifyAvailable'


class Status:
    approved = 'Approved'
    declined = 'Declined'
    init = 'Init'

    @classmethod
    def all(cls):
        return [cls.approved, cls.declined]


class Notification(BaseModel):
    id: int
    souring_id: Optional[int]
    sourcing_name: str
    status: str
    type: str

    status: str
    seen_status: str
    description: str

    from_hospital_id: Optional[int]
    to_hospital_id: Optional[int]

    created_at: Optional[datetime]


class BuyerSellerMap(BaseModel):
    sourcing_id: int
    sourcing_name: str

    from_hospital_id: int
    to_hospital_id: int

    created_at: Optional[datetime]


class NotificationItem(BaseModel):
    id: int
    trackingMedicine: str
    status: str
    type: str
    seenStatus: str
    from_hospital_id: Optional[int]
    to_hospital_id: Optional[int]


class NotificationWithHospital(Notification):
    from_hospital: Optional[Hospital]
    to_hospital: Optional[Hospital]
