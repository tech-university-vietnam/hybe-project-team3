from typing import List

import pinject
from fastapi import Header, Depends
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status

from app.controllers.tracking_medicine.model import TrackingMedicinePayload
from app.domains.medicine.medicine_service import MedicineService
from app.domains.user.user_service import UserService
from app.model.tracking_medicine import TrackingMedicine
from app.services.jwt_service import JWTService
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, HTTPAuthorizationCredentials

router = InferringRouter()
oauth2_scheme = HTTPBearer(scheme_name='token')


@cbv(router)
class TrackingMedicineRoute:

    def __init__(self):
        obj_graph = pinject.new_object_graph()
        self.medicine_service: MedicineService = obj_graph.provide(MedicineService)
        self.jwt_service: JWTService = obj_graph.provide(JWTService)
        self.user_service: UserService = obj_graph.provide(UserService)

    @router.get("/tracking-medicines", tags=["medicine"], response_model=List[TrackingMedicine])
    def list_trackings(self):
        test = list(map(lambda m: m.dict(), self.medicine_service.list()))
        return JSONResponse(test)

    @router.get("/tracking-medicine/{tracking_id}", tags=["medicine"], response_model=TrackingMedicine)
    def get_tracking(self, tracking_id: int):
        medicine = self.medicine_service.get(tracking_id)
        return JSONResponse(medicine.dict())

    @router.post("/tracking-medicine", tags=["medicine"], response_model=TrackingMedicine)
    async def create_tracking_medicine(self, payload: TrackingMedicinePayload,
                                       bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)

        medicine = self.medicine_service.create(payload, user)
        return JSONResponse(medicine.dict(), status.HTTP_201_CREATED)

    @router.put("/tracking-medicine/{tracking_id}", tags=["medicine"], response_model=TrackingMedicine)
    def update_tracking_medicine(self, tracking_id: int, payload: TrackingMedicinePayload):
        return self.medicine_service.update(tracking_id, payload)

    @router.delete("/tracking-medicine/{tracking_id}", tags=["medicine"], response_model=TrackingMedicine)
    def delete_tracking_medicine(self, tracking_id: int):
        success = self.medicine_service.delete(tracking_id)
        if success:
            return JSONResponse(None, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(None, status_code=status.HTTP_404_NOT_FOUND)