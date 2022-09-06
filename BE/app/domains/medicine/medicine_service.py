from app.controllers.tracking_medicine.model import TrackingMedicinePayload
from app.domains.medicine.medicine_repository import MedicineRepository


class MedicineService:

    def __init__(self, medicine_repository: MedicineRepository):
        self.medicine_repo = medicine_repository

    def get(self, id: int):
        return self.medicine_repo.get(id)

    def list(self):
        return self.medicine_repo.list()

    def create(self, payload: TrackingMedicinePayload):
        return self.medicine_repo.create(payload)

    def update(self, id: int, payload: TrackingMedicinePayload):
        return self.medicine_repo.update(id, payload)

    def delete(self, id: int):
        return self.medicine_repo.delete(id)
