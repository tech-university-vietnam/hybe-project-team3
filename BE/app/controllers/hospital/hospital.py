from typing import List
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.responses import JSONResponse
from app.controllers.hospital import schema
from fastapi import status
from app import register_class


router = InferringRouter()



class HospitalRoute:
    def __init__(self, hospital_service) -> None:
        self.hospital_service = hospital_service

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

@cbv(router)
class HospitalRoot(HospitalRoute):
    def __init__(self, hospital_service) -> None:
        super().__init__(hospital_service)


register_class(HospitalRoute)
