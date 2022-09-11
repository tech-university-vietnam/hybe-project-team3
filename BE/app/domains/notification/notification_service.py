from app.domains.source_order_request.source_order_request_repository import SourceOrderRequestRepository
from app.controllers.tracking_medicine.model import TrackingMedicinePayload
from app.domains.notification.notification_repository import NotificationRepository
from app.domains.medicine.medicine_repository import MedicineRepository


class NotificationService:

    def __init__(self,
                 notification_repository: NotificationRepository,
                 medicine_repository: MedicineRepository,
                 source_order_request_repository: SourceOrderRequestRepository):
        self.notification_repo = notification_repository
        self.medicine_repo = medicine_repository
        self.source_repo = source_order_request_repository

    def create(self, data):
        return self.notification_repo.create(data)

    def list(self, hospital_id):
        return self.notification_repo.list(hospital_id)

    def update(self, data, source_id, user_id):
        return self.notification_repo.update(data, source_id, user_id)

    def _is_created_by_user(self, user_id):
        return self.notification_repo.check_user_id(user_id)

    def delete(self, id, user_id):
        """
        If user has the same id as created_by id -> delete
        If not -> check if user is in the same id
        """
        try:
            return self.notification_repo.delete(id, user_id)
        except:
            raise PermissionError

    def get_notseen_number(self, hospital_id: int):
        return self.notification_repo.get_notseen_number(hospital_id)

    def update_status(self, noti_id: int, status: str, user_id: int, hospital_id: int):
        # update med status to listed
        # update notification status
        noti = self.notification_repo.update_status(noti_id, status)
        if noti.type == "warningExpired" and noti.status == 'Approved':
            self.medicine_repo.update(noti.sourcing_id, TrackingMedicinePayload(status="Listed"))
        if noti.type == "notifySold" and noti.status == 'Approved':
            self.medicine_repo.update(noti.tracking_medicine_id, TrackingMedicinePayload(status="Sold"))
            self.source_repo.update({"status": "Resolved"}, noti.sourcing_id, user_id)
