from app.controllers.tracking_medicine.model import TrackingMedicinePayload
from app.domains.medicine.medicine_repository import MedicineRepository
from app.model.user import DetailUser


class MedicineService:

    def __init__(self, medicine_repository: MedicineRepository):
        self.medicine_repo = medicine_repository

    def get(self, id: int):
        return self.medicine_repo.get(id)

    def list(self):
        return self.medicine_repo.list()

    def create(self, payload: TrackingMedicinePayload, user: DetailUser):
        return self.medicine_repo.create(payload, user)

    def get_listed_medicine_quantity(self, payload: TrackingMedicinePayload, user: DetailUser):

        # return self.medicine_repo.get_listed_medicine_quantity(payload, user)
        pass

    def update(self, id: int, payload: TrackingMedicinePayload):
        return self.medicine_repo.update(id, payload)

    def delete(self, id: int):
        return self.medicine_repo.delete(id)

