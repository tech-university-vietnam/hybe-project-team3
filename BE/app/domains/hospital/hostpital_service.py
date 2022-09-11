from app.domains.hospital.hospital_repository import HospitalRepository


class HospitalService:

    def __init__(self, hospital_repository: HospitalRepository):
        self.hospital_repo = hospital_repository

    def get_hospitals(self):
        return self.hospital_repo.get_hospitals()
