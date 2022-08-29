from typing import List
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.responses import JSONResponse
from app.controllers.hospital import schema
from app.domains.hospital.hostpital_service import HospitalService
import pinject
from fastapi import status
router = InferringRouter()


@cbv(router)
class HospitalRoute:
    def __init__(self) -> None:
        obj_graph = pinject.new_object_graph()
        self.hospital_service: HospitalService = obj_graph.provide(
            HospitalService)

    @router.get("/hospitals", tags=["hospitals"])
    def get_hospitals(self) -> List[schema.HospitalItem]:
        hospital_list = self.hospital_service.get_hospitals()
        return JSONResponse(content=hospital_list,
                            status_code=status.HTTP_200_OK)

    @router.get("/hospitals/seed", tags=["hospitals"])
    def seed_hospitals(self) -> schema.SeedResponse:
        self.hospital_service.hospital_seed()
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"msg": "success"})
