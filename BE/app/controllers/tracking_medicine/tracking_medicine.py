from typing import List

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status

from app.controllers.dependency_injections.container import Container
from app.controllers.tracking_medicine.model import TrackingMedicinePayload
from app.domains.medicine.medicine_service import MedicineService
from app.domains.user.user_service import UserService
from app.model.tracking_medicine import TrackingMedicine, TrackingMedicineWithHospital
from app.services.jwt_service import JWTService
from fastapi.security import HTTPAuthorizationCredentials
from app.main import oauth2_scheme
router = InferringRouter()


@cbv(router)
class TrackingMedicineRoute:

    def __init__(self):
        container = Container()
        self.medicine_service: MedicineService = container.medicine_service_factory()
        self.jwt_service: JWTService = container.jwt_service_factory()
        self.user_service: UserService = container.user_service_factory()

    @router.get("/tracking-medicines", tags=["medicine"],
                response_model=List[TrackingMedicine])
    def list_trackings(self, bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_detail_user_by_id(user_id)
        meds = self.medicine_service.list(user.work_for)
        return meds

    @router.get("/tracking-medicine/{tracking_id}", tags=["medicine"],
                response_model=TrackingMedicineWithHospital)
    def get_tracking(self, tracking_id: int):
        medicine = self.medicine_service.get(tracking_id)
        return medicine

    @router.post("/tracking-medicine", tags=["medicine"],
                 response_model=TrackingMedicine,
                 status_code=status.HTTP_201_CREATED)
    async def create_tracking_medicine(
        self,
        payload: TrackingMedicinePayload,
        bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_detail_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)

        medicine = self.medicine_service.create(payload, user)
        return medicine.dict()

    @router.put("/tracking-medicine/{tracking_id}", tags=["medicine"],
                response_model=TrackingMedicine)
    def update_tracking_medicine(self, tracking_id: int, payload:
                                 TrackingMedicinePayload):
        return self.medicine_service.update(tracking_id, payload)

    @router.delete("/tracking-medicine/{tracking_id}", tags=["medicine"],
                   response_model=TrackingMedicine)
    def delete_tracking_medicine(self, tracking_id: int):
        success = self.medicine_service.delete(tracking_id)
        if success:
            return JSONResponse(None, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(None, status_code=status.HTTP_404_NOT_FOUND)

