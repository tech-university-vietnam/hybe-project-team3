
import pinject
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status
from app.model.notification import NotificationIdPayload
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
      "type": "warningExpired",
      "hospitalName": "VinMec",
      "medicineName": "Advil",
      "status": "init",
      "seenStatus": "not seen"
    },
    {
      "id": 2,
      "type": "notifySold",
      "hospitalName": "VinMec",
      "medicineName": "Advil",
      "status": "init",
      "seenStatus": "not seen"
    },
    {
      "id": 3,
      "type": "notifyAvailable",
      "hospitalName": "VinMec",
      "medicineName": "Advil",
      "status": "init",
      "seenStatus": "not seen"
    },
    {
      "id": 4,
      "type": "warningExpired",
      "hospitalName": "VinMec",
      "medicineName": "Advil",
      "status": "approved",
      "seenStatus": "seen"
    },
    {
      "id": 5,
      "type": "warningExpired",
      "hospitalName": "VinMec",
      "medicineName": "Advil",
      "status": "declined",
      "seenStatus": "seen"
    },
    {
      "id": 6,
      "type": "notifyAvailable",
      "hospitalName": "VinMec",
      "medicineName": "Advil",
      "status": "approved",
      "seenStatus": "seen"
    },
  ]


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

    @router.get("/notifications", tags=["notification"],
                 status_code=status.HTTP_200_OK)
    def get_list(
        self,
        bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)
        for item in  DUMMY_NOTIFICATIONS:
            item['seenStatus'] = "seen"
        return DUMMY_NOTIFICATIONS

    @router.get("/notification/seed", tags=["notification"],
                 status_code=status.HTTP_200_OK)
    def seed(self):
        DUMMY_NOTIFICATIONS.append({
            "id": len(DUMMY_NOTIFICATIONS)+1,
            "type": "notifyAvailable",
            "hospitalName": "VinMec",
            "medicineName": "Advil",
            "status": "approved",
            "seenStatus": "not seen"
        })
        print(DUMMY_NOTIFICATIONS)
        return {"msg": "ok"}

    @router.post("/notification/approved", tags=["notification"],
                 status_code=status.HTTP_200_OK)
    def approved(
        self,
        payload: NotificationIdPayload,
        bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)
        DUMMY_NOTIFICATIONS[payload.id - 1]["status"] = "approved"
        return DUMMY_NOTIFICATIONS[payload.id - 1]


    @router.post("/notification/declined", tags=["notification"],
                 status_code=status.HTTP_200_OK)
    def declined(
        self,
        payload: NotificationIdPayload,
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

        DUMMY_NOTIFICATIONS[payload.id - 1]["status"] = "declined"
        return DUMMY_NOTIFICATIONS[payload.id - 1]

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
        count = 0
        for item in DUMMY_NOTIFICATIONS:
            if item['seenStatus'] == "not seen":
                count += 1
        return {"notseen_noti": count}
