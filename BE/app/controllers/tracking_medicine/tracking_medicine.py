from typing import List

import pinject
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status

from app.controllers.tracking_medicine.model import TrackingMedicinePayload
from app.domains.medicine.medicine_service import MedicineService
from app.domains.user.user_service import UserService
from app.model.tracking_medicine import TrackingMedicine
from app.services.jwt_service import JWTService
from fastapi.security import HTTPAuthorizationCredentials
from app.main import oauth2_scheme
router = InferringRouter()


@cbv(router)
class TrackingMedicineRoute:

    def __init__(self):
        obj_graph = pinject.new_object_graph()
        self.medicine_service: MedicineService = obj_graph.provide(
            MedicineService)
        self.jwt_service: JWTService = obj_graph.provide(JWTService)
        self.user_service: UserService = obj_graph.provide(UserService)

    @router.get("/tracking-medicines", tags=["medicine"],
                response_model=List[TrackingMedicine])
    def list_trackings(self,
                       bearer_auth:
                       HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_detail_user_by_id(user_id)
        meds = self.medicine_service.list(user.work_for)
        return meds

    @router.get("/tracking-medicine/{tracking_id}", tags=["medicine"],
                response_model=TrackingMedicine)
    def get_tracking(self, tracking_id: int):
        medicine = self.medicine_service.get(tracking_id)
        return medicine.dict()

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

    @router.patch("/tracking-medicine/{tracking_id}", tags=["medicine"],
                response_model=TrackingMedicine)
    def update_tracking_medicine(self, tracking_id: int, payload:
                                 TrackingMedicinePayload,
        bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_detail_user_by_id(user_id)
        return self.medicine_service.update(tracking_id, payload, user.work_for)

    @router.delete("/tracking-medicine/{tracking_id}", tags=["medicine"],
                   response_model=TrackingMedicine)
    def delete_tracking_medicine(self, tracking_id: int, bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_detail_user_by_id(user_id)
        success = self.medicine_service.delete(tracking_id, user.work_for)
        if success:
            return JSONResponse(None, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(None, status_code=status.HTTP_404_NOT_FOUND)

