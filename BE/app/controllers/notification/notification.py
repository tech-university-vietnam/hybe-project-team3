
import pinject
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status
from app.model.notification import NotificationActionPayload

from app.domains.medicine.medicine_service import MedicineService
from app.domains.user.user_service import UserService
from app.controllers.common.schema import CommonResponse
from app.services.jwt_service import JWTService
from fastapi.security import HTTPAuthorizationCredentials
from app.main import oauth2_scheme
router = InferringRouter()

DUMMY_NOTIFICATIONS = [
    {
        "id": 1,
        "status": "init",
        "name": "panadol",
        "hospitalName": "Hồ Chí Minh city 115 Emergency center",
        "type": "warningExpired"
    },
    {
        "id": 2,
        "status": "aprroved",
        "name": "panadol",
        "hospitalName": "Hồ Chí Minh city 115 Emergency center",
        "type": "warningExpired"
    },
    {
        "id": 3,
        "status": "declined",
        "name": "panadol",
        "hospitalName": "Hồ Chí Minh city 115 Emergency center",
        "type": "warningExpired"
    },
    {
        "id": 4,
        "status": "init",
        "name": "panadol",
        "hospitalName": "Hồ Chí Minh city 115 Emergency center",
        "type": "notifySold"
    },
    {
        "id": 5,
        "status": "approved",
        "name": "panadol",
        "hospitalName": "Hồ Chí Minh city 115 Emergency center",
        "type": "notifySold"
    },
    {
        "id": 6,
        "status": "declined",
        "name": "panadol",
        "hospitalName": "Hồ Chí Minh city 115 Emergency center",
        "type": "notifySold"
    },
    {
        "id": 7,
        "status": "init",
        "name": "panadol",
        "hospitalName": "Hồ Chí Minh city 115 Emergency center",
        "type": "notifyAvailable"
    },
    {
        "id": 8,
        "name": "panadol",
        "status": "approved",
        "hospitalName": "Hồ Chí Minh city 115 Emergency center",
        "type": "notifyAvailable"
    },
    {
        "id": 9,
        "status": "declined",
        "name": "panadol",
        "hospitalName": "Hồ Chí Minh city 115 Emergency center",
        "type": "notifyAvailable"
    }
]


@cbv(router)
class NotificationRoute:

    def __init__(self):
        obj_graph = pinject.new_object_graph()
        self.medicine_service: MedicineService = obj_graph.provide(
            MedicineService)
        self.jwt_service: JWTService = obj_graph.provide(JWTService)
        self.user_service: UserService = obj_graph.provide(UserService)

    @router.get("/notifications", tags=["notification"],
                 status_code=status.HTTP_200_OK)
    def get(
        self,
        bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)

        return DUMMY_NOTIFICATIONS

    @router.post("/notification/approve", tags=["notification"],
                 status_code=status.HTTP_200_OK,
                 response_model=CommonResponse)
    def approve(
        self,
        payload: NotificationActionPayload,
        bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)
        return {"msg": "ok"}


    @router.post("/notification/decline", tags=["notification"],
                 status_code=status.HTTP_200_OK,
                 response_model=CommonResponse)
    def decline(
        self,
        payload: NotificationActionPayload,
        bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
        """
        change status to Resolved in tracking medicine if type warningExpired
        dont change status if type nofitySold
        Has type in payload
        """

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)

        return {"msg": "ok"}