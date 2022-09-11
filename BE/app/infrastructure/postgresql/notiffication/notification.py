from datetime import datetime
from typing import Union

from sqlalchemy import Column, String, DateTime, Integer, Index
from sqlalchemy.orm import relationship

from app.infrastructure.postgresql.database import Base
from app.infrastructure.postgresql.hospital.hospital import HospitalDTO
from app.infrastructure.postgresql.tracking_medicine.tracking_medicine import TrackingMedicineDTO
from app.model.notification import Notification, SeenStatus, SourceType, Status, NotificationWithHospital


class NotificationDTO(Base):
    """userDTO is a data transfer object associated with User entity."""

    __tablename__ = "Notification"
    id: Union[int, Column] = Column(Integer, primary_key=True,
                                    autoincrement=True)

    # For joining with TrackingMedicine or SourceOrder
    sourcing_id: Union[int, Column] = Column(Integer)
    # `tracking` for tracking-medicine, `source-order` for source order request
    sourcing_type: Union[str, Column] = Column(String)
    # Both seller and buyer
    sourcing_name: Union[str, Column] = Column(String)

    status: Union[str, Column] = Column(String)  # Approve/Reject button, init when first created
    seen_status: Union[str, Column] = Column(String, default=SeenStatus.not_seen)
    description: Union[str, Column] = Column(String)  # Text shown in UI

    # For buyer
    from_hospital_id: Union[int, Column] = Column(Integer, nullable=True)
    to_hospital_id: Union[int, Column] = Column(Integer, nullable=True)

    from_hospital: HospitalDTO = relationship("HospitalDTO", viewonly=True, uselist=False,
                                              primaryjoin='NotificationDTO.from_hospital_id == foreign(HospitalDTO.id)')

    to_hospital: HospitalDTO = relationship("HospitalDTO", viewonly=True, uselist=False,
                                            primaryjoin='NotificationDTO.to_hospital_id == foreign(HospitalDTO.id)')

    created_at: Union[datetime, Column] = Column(DateTime, default=datetime.now(), nullable=True)

    Index('idx_notification_sourcing_', sourcing_type, sourcing_id, unique=True)

    def to_entity(self) -> Notification:
        return Notification(
            id=self.id,
            sourcing_id=self.sourcing_id,
            sourcing_type=self.sourcing_type,
            sourcing_name=self.sourcing_name,
            status=self.status,
            seen_status=self.seen_status,
            description=self.description,
            from_hospital_id=self.from_hospital_id,
            to_hospital_id=self.to_hospital_id,
            created_at=self.created_at,
        )

    def to_full_entity(self) -> NotificationWithHospital:
        return NotificationWithHospital(
            id=self.id,
            sourcing_id=self.sourcing_id,
            sourcing_type=self.sourcing_type,
            sourcing_name=self.sourcing_name,
            status=self.status,
            seen_status=self.seen_status,
            description=self.description,
            from_hospital_id=self.from_hospital_id,
            to_hospital_id=self.to_hospital_id,
            from_hospital=self.from_hospital and self.from_hospital.to_entity(),
            to_hospital=self.to_hospital and self.to_hospital.to_entity(),
            created_at=self.created_at,
        )

    @classmethod
    def from_tracking_medicine(cls, med: TrackingMedicineDTO):
        return cls(
            sourcing_id=med.id,
            sourcing_type=SourceType.tracking,
            sourcing_name=med.name,
            status=Status.init,
            description='',
            from_hospital_id=med.hospital_id,
            to_hospital_id=None
        )

    @classmethod
    def from_notification_payload(cls, payload: Notification):
        return cls(
            sourcing_id=payload.souring_id,
            sourcing_type=payload.sourcing_type,
            sourcing_name=payload.sourcing_name,
            status=payload.status,
            description=payload.description,
            from_hospital_id=payload.from_hospital_id,
            to_hospital_id=payload.to_hospital_id
        )
