from datetime import datetime
from optparse import Option

from typing import Optional

from pydantic import BaseModel


class SourceOrderRequest(BaseModel):
    id: int
    status: str
    name: str


class SourceOrderRequestPayload(BaseModel):
    name: str
    created_by: Optional[int]
    status: Optional[str]


class SourceOrderRequestUpdatePayload(BaseModel):
    status: Optional[str]

