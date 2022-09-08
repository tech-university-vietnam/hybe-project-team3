from typing import Optional
from pydantic import BaseModel


class NotificationActionPayload(BaseModel):
    id: int
    type: str
