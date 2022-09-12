from typing import List

from app.domains.source_order_request.source_order_request_repository import SourceOrderRequestRepository
from app.controllers.tracking_medicine.model import TrackingMedicinePayload
from app.domains.notification.notification_repository import NotificationRepository
from app.domains.medicine.medicine_repository import MedicineRepository
from app.model.notification import Type, Status


class NotificationService:

    def __init__(self,
                 notification_repository: NotificationRepository,
                 medicine_repository: MedicineRepository,
                 source_order_request_repository: SourceOrderRequestRepository):
        self.noti_repo = notification_repository
        self.medicine_repo = medicine_repository
        self.source_repo = source_order_request_repository

    def create(self, data):
        return self.noti_repo.create(data)

    def list(self, hospital_id):
        return self.noti_repo.list(hospital_id)

    def update(self, data, source_id, user_id):
        return self.noti_repo.update(data, source_id, user_id)

    def delete(self, id, user_id):
        """
        If user has the same id as created_by id -> delete
        If not -> check if user is in the same id
        """
        pass

    def count_total_not_seen(self, hospital_id: int):
        return self.noti_repo.count_total_not_seen(hospital_id)

    def update_status(self, noti_id: int, status: str, user_id: int, hospital_id: int):
        # update med status to listed
        # update notification status
        noti = self.noti_repo.update_status(noti_id, status)
        if noti and noti.type == Type.warning_expired and noti.status == Status.approved:
            self.medicine_repo.update_status(noti.sourcing_id,"Listed", hospital_id)

        if noti and noti.type == Type.notify_sold and noti.status == Status.approved:
            self.medicine_repo.update_status(noti.tracking_medicine_id, TrackingMedicinePayload(status="Sold"))
            self.source_repo.update({"status": "Resolved"}, noti.sourcing_id, hospital_id)
        return noti

    def update_all_seen_status(self, ids: List[int]):
        return self.noti_repo.update_all_seen_status(ids)
