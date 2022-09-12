from typing import List

import pinject
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.controllers.hospital import schema
from app.domains.hospital.hostpital_service import HospitalService

router = InferringRouter()


@cbv(router)
class HospitalRoute:
    def __init__(self) -> None:
        obj_graph = pinject.new_object_graph()
        self.hospital_service: HospitalService = obj_graph.provide(HospitalService)

    @router.get("/hospitals", tags=["hospitals"])
    def get_hospitals(self) -> List[schema.HospitalItem]:
        hospital_list = self.hospital_service.get_hospitals()
        return JSONResponse(content=hospital_list,
                            status_code=status.HTTP_200_OK)
