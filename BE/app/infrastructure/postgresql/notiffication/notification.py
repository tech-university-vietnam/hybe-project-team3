from datetime import datetime
from typing import Union

from sqlalchemy import Column, String, DateTime, Integer, Index
from sqlalchemy.orm import relationship
from app.model.notification import NotificationItem, Type

from app.infrastructure.postgresql.database import Base
from app.infrastructure.postgresql.hospital.hospital import HospitalDTO
from app.infrastructure.postgresql.tracking_medicine.tracking_medicine import TrackingMedicineDTO
from app.model.notification import Notification, SeenStatus, Status, NotificationWithHospital


class NotificationDTO(Base):
    __tablename__ = "Notification"
    id: Union[int, Column] = Column(Integer, primary_key=True,
                                    autoincrement=True)

    # For joining with TrackingMedicine or SourceOrder
    sourcing_id: Union[int, Column] = Column(Integer)
    # Both seller and buyer, medicine_name
    sourcing_name: Union[str, Column] = Column(String)

    # warningExpired, notifySold, notifyAvailable
    type: Union[str, Column] = Column(String, nullable=False)

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

    tracking_medicine_id: Union[int, Column] = Column(Integer, nullable=True)

    # Index('idx_notification_sourcing_', type, sourcing_id, unique=False)

    def to_entity(self) -> Notification:
        return Notification(
            id=self.id,
            sourcing_id=self.sourcing_id,
            sourcing_name=self.sourcing_name,
            type=self.type,
            status=self.status,
            seen_status=self.seen_status,
            description=self.description,
            from_hospital_id=self.from_hospital_id,
            to_hospital_id=self.to_hospital_id,
            created_at=self.created_at,
        )

    @classmethod
    def from_sourcing_entity(cls, source_id, med_id, med_name, med_from, med_to):
        return cls(
            sourcing_id=source_id,
            tracking_medicine_id=med_id,
            sourcing_name=med_name,
            status=Status.init,
            description='',
            from_hospital_id=med_from,
            to_hospital_id=med_to,
            type=Type.notify_available
        )

    @classmethod
    def from_approved_request(cls, noti: "NotificationDTO"):
        return cls(
            sourcing_id=noti.sourcing_id,
            tracking_medicine_id=noti.tracking_medicine_id,
            sourcing_name=noti.sourcing_name,
            status=Status.init,
            description='',
            from_hospital_id=noti.from_hospital_id,
            to_hospital_id=noti.to_hospital_id,
            type=Type.notify_sold
        )

    def to_full_entity(self) -> NotificationWithHospital:
        return NotificationWithHospital(
            id=self.id,
            sourcing_id=self.sourcing_id,
            sourcing_name=self.sourcing_name,
            type=self.type,
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
            sourcing_name=med.name,
            status=Status.init,
            description='',
            from_hospital_id=med.hospital_id,
            to_hospital_id=None,
            type=Type.warning_expired
        )


    def to_list_item(self) -> NotificationItem:
        return NotificationItem(
            id=self.id,
            type=self.type,
            status=self.status,
            trackingMedicine=self.sourcing_name,
            seenStatus=self.seen_status,
            from_hospital_id=self.from_hospital_id,
            to_hospital_id=self.to_hospital_id
        )

    @classmethod
    def from_notification_payload(cls, payload: Notification):
        return cls(
            sourcing_id=payload.souring_id,
            sourcing_name=payload.sourcing_name,
            status=payload.status,
            description=payload.description,
            from_hospital_id=payload.from_hospital_id,
            to_hospital_id=payload.to_hospital_id
        )
