from datetime import datetime
from typing import Union

from sqlalchemy import Column, String, DateTime, Integer, Index

from app.infrastructure.postgresql.database import Base
from app.infrastructure.postgresql.tracking_medicine.tracking_medicine import TrackingMedicineDTO
from app.model.notification import Notification
from app.model.tracking_medicine import TrackingMedicine


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
    seen_status: Union[str, Column] = Column(String, default='Not seen')
    description: Union[str, Column] = Column(String)  # Text shown in UI

    # For buyer
    from_hospital_id: Union[int, Column] = Column(Integer, nullable=True)
    to_hospital_id: Union[int, Column] = Column(Integer, nullable=True)

    created_at: Union[datetime, Column] = Column(DateTime, default=datetime.now(), nullable=True)

    Index('idx_notification_sourcing_', sourcing_type, sourcing_id, unique=True)

    def to_entity(self) -> Notification:
        return Notification(
            id=self.id,
            sourcing_id=self.sourcing_id,
            sourcing_type=self.sourcing_type,
            sourcing_name=self.sourcing_name,
            status=self.status,
            description=self.description,
            from_hospital_id=self.from_hospital_id,
            to_hospital_id=self.to_hospital_id,
            created_at=self.created_at,
        )

    @classmethod
    def from_tracking_medicine(cls, med: TrackingMedicineDTO):
        return cls(
            sourcing_id=med.id,
            sourcing_type='tracking',
            sourcing_name=med.name,
            status='Init',
            description='',
            from_hospital_id=med.hospital_id,
            to_hospital_id=None
        )

    # @classmethod
    # def from_notification_payload(cls, payload: NotificationPayload):
    #     return cls(
    #         name=medicine.name,
    #         number=medicine.number,
    #         status=medicine.status,
    #         buy_price=medicine.buy_price,
    #         manufacturer=medicine.manufacturer,
    #         expired_date=medicine.expired_date,
    #         created_at=medicine.created_at,
    #         created_by=medicine.created_by,
    #         image=medicine.image,
    #         hospital_id=medicine.hospital_id,
    #     )
