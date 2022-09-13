from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.model.hospital import Hospital


class TrackingMedicine(BaseModel):
    id: int
    name: str
    number: Optional[int]
    status: str

    expired_date: datetime


class TrackingMedicineWithHospital(TrackingMedicine):
    hospital: Optional[Hospital]