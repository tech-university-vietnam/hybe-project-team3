from app.controllers.tracking_medicine.model import TrackingMedicinePayload
from app.domains.medicine.medicine_repository import MedicineRepository
from app.model.user import DetailUser


class MedicineService:

    def __init__(self, medicine_repository: MedicineRepository):
        self.medicine_repo = medicine_repository

    def get(self, id: int):
        return self.medicine_repo.get(id)

    def list(self, hospital_id: int):
        return self.medicine_repo.list(hospital_id)

    def create(self, payload: TrackingMedicinePayload, user: DetailUser):
        return self.medicine_repo.create(payload, user)

    def get_listed_medicine_quantity(self, payload: TrackingMedicinePayload, user: DetailUser):

        # return self.medicine_repo.get_listed_medicine_quantity(payload, user)
        pass

    def update(self, id: int, payload):
        return self.medicine_repo.update(id, payload)

    def update_status(self, id: int, status, hospital_id: int):
        return self.medicine_repo.update(id, status, hospital_id)

    def delete(self, id: int, hospital_id: int):
        return self.medicine_repo.delete(id, hospital_id)

