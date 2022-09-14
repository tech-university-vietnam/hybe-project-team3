from datetime import datetime
from optparse import Option

from typing import Optional

from pydantic import BaseModel

from app.model.hospital import Hospital


class SourceOrderRequest(BaseModel):
    id: int
    status: str
    name: str


class SourceOrderHospitalRequest(BaseModel):
    id: int
    status: str
    name: str
    created_at: datetime
    hospital: Optional[Hospital]


class SourceOrderRequestPayload(BaseModel):
    name: str
    created_by: Optional[int]
    status: Optional[str]
    hospital_id: Optional[int]


class SourceOrderRequestUpdatePayload(BaseModel):
    status: Optional[str]


class SourceStatus:
    available = "Available"
    unavailable = "Unavailable"
    resolved = "Resolved"
