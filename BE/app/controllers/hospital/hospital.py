from typing import List

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.controllers.dependency_injections.container import Container
from app.controllers.hospital import schema
from app.domains.hospital.hostpital_service import HospitalService

router = InferringRouter()


@cbv(router)
class HospitalRoute:
    def __init__(self) -> None:
        container = Container()
        self.hospital_service: HospitalService = container.hospital_service_factory()

    @router.get("/hospitals", tags=["hospitals"])
    def get_hospitals(self) -> List[schema.HospitalItem]:
        hospital_list = self.hospital_service.get_hospitals()
        return hospital_list
