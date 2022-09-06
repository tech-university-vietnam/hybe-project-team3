from .hospital_repository import HospitalRepository
from app import register_class
from .hostpital_service import HospitalService

register_class(HospitalRepository)
register_class(HospitalService)