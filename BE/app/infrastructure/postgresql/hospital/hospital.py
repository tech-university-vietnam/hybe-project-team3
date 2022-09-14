from datetime import datetime
from typing import Union

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import relationship
from app.model.hospital import HospitalItem
from app.infrastructure.postgresql.database import Base
from app.model.hospital import Hospital


class HospitalDTO(Base):
    """hospitalDTO is a data transfer object associated with User entity."""

    __tablename__ = "Hospital"
    id: Union[int, Column] = Column(Integer, primary_key=True,
                                    autoincrement=True)

    name: Union[str, Column] = Column(String, nullable=True)
    telephone: Union[str, Column] = Column(String, nullable=False)
    # Auth data
    address: Union[str, Column] = Column(String, nullable=False)
    join_date: Union[datetime, Column] = Column(DateTime(timezone=True),
                                                nullable=True)
    users = relationship("UserDTO", backref=__tablename__, uselist=True)

    def to_entity(self) -> Hospital:
        return Hospital(
            id=self.id,
            name=self.name,
            telephone=self.telephone,
            address=self.address,
            join_date=self.join_date,
        )

    def to_entity_item(self) -> HospitalItem:
        return HospitalItem(id=self.id, name=self.name)

    @staticmethod
    def from_entity(hospital: Hospital) -> "HospitalDTO":
        now = datetime.utcnow()
        return HospitalDTO(
            id=hospital.id,
            name=hospital.name,
            telephone=hospital.telephone,
            address=hospital.address,
            join_date=now,
        )

    @staticmethod
    def from_mock_data(
            name: str, telephone: str, address: str) -> "HospitalDTO":
        now = datetime.utcnow()
        return HospitalDTO(
            name=name,
            telephone=telephone,
            address=address,
            join_date=now,
        )
