from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.model.hospital import Hospital


class Status:
    sold = 'Sold'
    listing = 'Listing'
    expired = 'Expired'
    not_listed = 'Not listed'
    finished_listing = 'Finished listing'


class TrackingMedicine(BaseModel):
    id: int
    name: str
    number: Optional[int]
    status: str

    expired_date: datetime


class TrackingMedicineWithHospital(TrackingMedicine):
    hospital: Optional[Hospital]


class MedicineStatus:
    listed = "Listed"
    finished_listing = "Finished listing"
    not_listed = "Not listed"