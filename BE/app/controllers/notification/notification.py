from typing import List

import pinject
from fastapi import Depends, Path, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from pydantic import BaseModel
from starlette import status

from app.domains.notification.notification_service import NotificationService
from app.model.notification import Notification
from app.domains.medicine.medicine_service import MedicineService
from app.domains.user.user_service import UserService
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

class TotalNotSeenPayload(BaseModel):
    total: int

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
        self.notify_service: NotificationService = obj_graph.provide(NotificationService)

    @router.get("/notifications", tags=["notification"],
                status_code=status.HTTP_200_OK, response_model=List[Notification])
    def get_list(self, background_tasks: BackgroundTasks,
                 bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)

        notifies = self.notify_service.list()

        ids_to_update = list(map(lambda noti: noti.id, notifies))
        background_tasks.add_task(self.notify_service.update_all_seen_status, ids_to_update)

        return notifies

    @router.get("/notification/seed", tags=["notification"],
                status_code=status.HTTP_200_OK)
    def seed(self):
        DUMMY_NOTIFICATIONS.append({
            "id": len(DUMMY_NOTIFICATIONS) + 1,
            "type": "notifyAvailable",
            "hospitalName": "VinMec",
            "medicineName": "Advil",
            "status": "approved",
            "seenStatus": "not seen"
        })
        print(DUMMY_NOTIFICATIONS)
        return {"msg": "ok"}

    @router.post("/notification/{id}/approved", tags=["notification"],
                 status_code=status.HTTP_200_OK)
    def approved(
            self,
            id: int = Path("Notification ID"),
            bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)

        return self.notify_service.approved(id)

    @router.post("/notification/{id}/declined", tags=["notification"],
                 status_code=status.HTTP_200_OK)
    def declined(self, id: int = Path("Notification ID"),
                 bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
        """
        change status to Resolved in tracking medicine if type warningExpired
        dont change status if type notifySold
        Has type in payload
        """

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)

        return self.notify_service.declined(id)

    @router.get("/notification/not-seen", tags=["notification"],
                status_code=status.HTTP_200_OK, response_model=TotalNotSeenPayload)
    def count_total_not_seen(
            self,
            bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
        """
        change status to Resolved in tracking medicine if type warningExpired
        dont change status if type notifySold
        Has type in payload
        """

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)

        total = self.notify_service.count_total_not_seen()

        return TotalNotSeenPayload(total=total)


