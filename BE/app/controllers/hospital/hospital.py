from typing import List
from fastapi_utils.inferring_router import InferringRouter
from fastapi.responses import JSONResponse
from app import inject
from app.controllers.hospital import schema
from app.domains.hospital import HospitalService
from fastapi import status
from app import register_class
from fastapi_utils.cbv import cbv

router = InferringRouter()


@cbv(router)
class HospitalRoute:

    @property
    def hospital_service(self) -> HospitalService:
        return inject(HospitalService)

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


register_class(HospitalRoute)
