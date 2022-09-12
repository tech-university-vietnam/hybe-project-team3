import pinject
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status
from app.domains.notification.notification_service import NotificationService
from app.model.notification import NotificationIdPayload
from app.domains.medicine.medicine_service import MedicineService
from app.domains.user.user_service import UserService
from app.controllers.common.schema import CommonResponse
from app.services.jwt_service import JWTService
from fastapi.security import HTTPAuthorizationCredentials
from app.main import oauth2_scheme

router = InferringRouter()


@cbv(router)
class NotificationRoute:
    """"
    inlcude status view
    add seen column
    return type
    """

    def __init__(self):
        obj_graph = pinject.new_object_graph()
        self.medicine_service: MedicineService = obj_graph.provide(
            MedicineService)
        self.jwt_service: JWTService = obj_graph.provide(JWTService)
        self.user_service: UserService = obj_graph.provide(UserService)
        self.notification_service: NotificationService = obj_graph.provide(
            NotificationService)

    @router.get("/notifications", tags=["notification"],
                status_code=status.HTTP_200_OK)
    def get_list(
            self,
            bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)
        return self.notification_service.list(user.work_for)

    @router.post("/notification/approved", tags=["notification"],
                 status_code=status.HTTP_200_OK)
    def approved(
            self,
            payload: NotificationIdPayload,
            bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)) -> CommonResponse:

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)
        self.notification_service.update_status(payload.id, "Approved", user.id, user.work_for)
        return {"msg": "success"}

    @router.post("/notification/declined", tags=["notification"],
                 status_code=status.HTTP_200_OK)
    def declined(
            self,
            payload: NotificationIdPayload,
            bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)) -> CommonResponse:
        """
        change status to Resolved in tracking medicine if type warningExpired
        dont change status if type nofitySold
        Has type in payload
        """

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)
        self.notification_service.update_status(payload.id, "Declined", user.id, user.work_for)

        return {"msg": "success"}

    @router.get("/notification/notseen", tags=["notification"],
                status_code=status.HTTP_200_OK)
    def get_notseen_notification(
            self,
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
        notseen_number = self.notification_service.get_notseen_number(user.work_for)
        return {"notseen_noti": notseen_number}
