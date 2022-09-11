from datetime import datetime
from typing import Union
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey

from app.model.source_order_request import SourceOrderRequest
from app.infrastructure.postgresql.database import Base


class SourceOrderRequestDTO(Base):
    """
        source_order_requestDTO is a data transfer object
        associated with source order request entity.
    """

    __tablename__ = "SourceOrderRequest"
    id: Union[int, Column] = Column(Integer, primary_key=True,
                                    autoincrement=True)

    name: Union[str, Column] = Column(String, nullable=False)
    status: Union[str, Column] = Column(String, default="Unavailable", nullable=True)
    created_by: Union[int, Column] = Column(Integer, ForeignKey("User.id"))
    created_at: Union[datetime, Column] = Column(DateTime, default=datetime.now(), nullable=True)
    updated_at: Union[datetime, Column] = Column(DateTime, default=datetime.now(), nullable=True)
    hospital_id: Union[int, Column] = Column(Integer, default=2, nullable=True)

    def to_entity(self) -> SourceOrderRequest:
        return SourceOrderRequest(
            id=self.id,
            name=self.name,
            status=self.status,
        )

    @classmethod
    def from_data(cls, data) -> "SourceOrderRequestDTO":
        return cls(
            name=data.name,
            status=data.status,
            created_by=data.created_by,
        )
