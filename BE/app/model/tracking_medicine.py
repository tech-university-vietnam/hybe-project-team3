from pydantic import BaseModel


class TrackingMedicine(BaseModel):
    id: int
    name: str
    number: int
    status: str
