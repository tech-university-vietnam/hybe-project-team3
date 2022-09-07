from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TrackingMedicinePayload(BaseModel):
    name: str
    number: Optional[int]
    status: Optional[str]
    buy_price: Optional[float]
    manufacturer: Optional[int]
    expired_date: datetime
    created_at: Optional[datetime]
    created_by: Optional[int]
    image: Optional[str]
    hospital_id: Optional[int]