from typing import List
from app.model.tracking_medicine import MedicineStatus
from app.model.source_order_request import SourceStatus

from fastapi import BackgroundTasks
from app.domains.source_order_request.source_order_request_repository import SourceOrderRequestRepository
from app.controllers.tracking_medicine.model import TrackingMedicinePayload
from app.domains.notification.notification_repository import NotificationRepository
from app.domains.medicine.medicine_repository import MedicineRepository
from app.model.notification import Type, Status
from app.model.tracking_medicine import Status as TrackingStatus


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

    def check_available_medicine(self, med_id):
        # Check tracking medicine exist
        if not med_id:
            # Skip check if noti does not have tracking_med_id
            return True

        medicine = self.medicine_repo.get(med_id)
        if not medicine or (medicine and medicine.status in [TrackingStatus.sold, TrackingStatus.expired,
                                                             TrackingStatus.finished_listing]):
            return False
        return True

    def update_status(self, noti_id: int, status: str, user_id: int, background_task: BackgroundTasks):

        # update med status to listed
        # update notification status
        noti = self.noti_repo.update_status(noti_id, status)

        med_available = self.check_available_medicine(noti.tracking_medicine_id)
        if not med_available:
            raise Exception('Medicine not available or removed')

        if noti and noti.type == Type.warning_expired and noti.status == Status.approved:
            self.medicine_repo.update(noti.sourcing_id, TrackingMedicinePayload(status="Listed"))

        if noti and noti.type == Type.notify_available:
            if noti.status == Status.approved:
                self.medicine_repo.update(noti.tracking_medicine_id, TrackingMedicinePayload(status=MedicineStatus.finished_listing))
                self.source_repo.update({"status": SourceStatus.resolved}, noti.sourcing_id, user_id)
                self.noti_repo.update_status_to_invalid(noti.tracking_medicine_id)
            if noti.status == Status.declined and not self.noti_repo.check_if_any_noti_exists(noti.sourcing_id):
                self.source_repo.update({"status": SourceStatus.unavailable}, noti.sourcing_id, noti.to_hospital_id)

        return noti

    def update_all_seen_status(self, ids: List[int]):
        return self.noti_repo.update_all_seen_status(ids)

    def check_if_any_noti_exists(self, sourcing_id: int):
        return self.noti_repo.check_if_any_noti_exists(sourcing_id)
