from datetime import datetime
from typing import Union

from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.orm import relationship

from app.controllers.tracking_medicine.model import TrackingMedicinePayload
from app.infrastructure.postgresql.database import Base
from app.infrastructure.postgresql.hospital.hospital import HospitalDTO
from app.model.tracking_medicine import TrackingMedicine, TrackingMedicineWithHospital
from app.infrastructure.postgresql.source_order_request.source_order_request import SourceOrderRequestDTO


class TrackingMedicineDTO(Base):

    __tablename__ = "TrackingMedicine"
    __allow_unmapped__ = True

    id: Union[int, Column] = Column(Integer, primary_key=True,
                                    autoincrement=True)

    name: Union[str, Column] = Column(String)
    number: Union[int, Column] = Column(Integer, nullable=True)
    status: Union[str, Column] = Column(String, nullable=False)
    buy_price: Union[float, Column] = Column(Float, nullable=True)
    manufacturer: Union[int, Column] = Column(Integer, nullable=True)
    expired_date: Union[datetime, Column] = Column(DateTime, nullable=False)
    created_at: Union[datetime, Column] = Column(DateTime,
                                                 default=datetime.utcnow,
                                                 nullable=True)
    created_by: Union[int, Column] = Column(Integer, nullable=False)
    image: Union[str, Column] = Column(String, nullable=True)
    hospital_id: Union[int, Column] = Column(Integer, nullable=False)

    hospital: HospitalDTO = relationship("HospitalDTO", viewonly=True, uselist=False,
                                         primaryjoin='TrackingMedicineDTO.hospital_id == foreign(HospitalDTO.id)')

    def to_entity(self) -> TrackingMedicine:
        return TrackingMedicine(
            id=self.id,
            name=self.name,
            number=self.number,
            status=self.status,
            expired_date=self.expired_date,

        )

    def to_full_entity(self) -> TrackingMedicineWithHospital:
        return TrackingMedicineWithHospital(
            id=self.id,
            name=self.name,
            number=self.number,
            status=self.status,
            expired_date=self.expired_date,
            hospital=self.hospital and self.hospital.to_entity()
        )

    @classmethod
    def from_tracking_medicine_payload(cls, medicine: TrackingMedicinePayload):
        return cls(
            name=medicine.name,
            number=medicine.number,
            status=medicine.status,
            buy_price=medicine.buy_price,
            manufacturer=medicine.manufacturer,
            expired_date=medicine.expired_date,
            created_at=medicine.created_at,
            created_by=medicine.created_by,
            image=medicine.image,
            hospital_id=medicine.hospital_id,
        )
