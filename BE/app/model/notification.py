from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Notification(BaseModel):
    id: int

    souring_id: int
    sourcing_type: str
    sourcing_name: str

    from_hospital_id: Optional[int]
    to_hospital_id: Optional[int]

    created_at: datetime
