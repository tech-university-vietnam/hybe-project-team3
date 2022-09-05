from app.controllers.tracking_medicine.model import TrackingMedicinePayload
from app.domains.medicine.medicine_repository import MedicalRepository


class MedicineService:

    def __init__(self, medical_repository: MedicalRepository):
        self.medical_repo = medical_repository

    def get(self, id: int):
        return self.medical_repo.get(id)

    def list(self):
        return list(map(lambda medicine: medicine.to_entity(), self.medical_repo.list()))

    def create(self, payload: TrackingMedicinePayload):
        return self.medical_repo.create(payload)

    def update(self, id: int, payload: TrackingMedicinePayload):
        return self.medical_repo.update(id, payload)
