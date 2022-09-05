from datetime import datetime

from pydantic import BaseModel

from app.model.tracking_medicine import TrackingMedicine


class TrackingMedicinePayload(BaseModel):
    name: str
    number: int
    status: str
    buy_price: float
    manufacturer: int
    expired_date: datetime
    created_at: datetime
    created_by: int
    image: str
    hospital_id: int