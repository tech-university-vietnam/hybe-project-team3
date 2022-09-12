from typing import List

import pinject
from fastapi import Depends, Path, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from pydantic import BaseModel
from starlette import status

from app.controllers.notification.schema import NotificationPayload
from app.domains.medicine.medicine_service import MedicineService
from app.domains.notification.notification_service import NotificationService
from app.domains.user.user_service import UserService
from app.main import oauth2_scheme
from app.model.notification import NotificationWithHospital, Status, SeenStatus, Type
from app.services.jwt_service import JWTService
from fastapi.security import HTTPAuthorizationCredentials


router = InferringRouter()


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
                status_code=status.HTTP_200_OK, response_model=List[NotificationWithHospital])
    def get_list(self, background_tasks: BackgroundTasks,
                 bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_detail_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)

        notifies = self.notify_service.list(user.work_for)

        ids_to_update = list(map(lambda noti: noti.id, notifies))
        background_tasks.add_task(self.notify_service.update_all_seen_status, ids_to_update)

        return notifies

    @router.get("/notification/seed", tags=["notification"],
                status_code=status.HTTP_201_CREATED)
    def seed(self):
        noti = [NotificationPayload(
            type=Type.notify_available,
            sourcing_name='Seed',
            status=Status.init,
            seen_status=SeenStatus.not_seen,
            description='Description available',
            from_hospital_id=1,
            to_hospital_id=5,
        ), NotificationPayload(
            type=Type.warning_expired,
            sourcing_name='Seed',
            status=Status.init,
            seen_status=SeenStatus.not_seen,
            description='Description expired',
            from_hospital_id=1,
            to_hospital_id=5,
        ), NotificationPayload(
            type=Type.notify_sold,
            sourcing_name='Seed',
            status=Status.init,
            seen_status=SeenStatus.not_seen,
            description='Description sold',
            from_hospital_id=1,
            to_hospital_id=5,
        )]
        self.notify_service.create(noti)
        return {"msg": "ok"}

    @router.post("/notification/{id}/approved", tags=["notification"],
                 status_code=status.HTTP_200_OK)
    def approved(
            self,
            background_tasks: BackgroundTasks,
            id: int = Path("Notification ID"),
            bearer_auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):

        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)

        notify = self.notify_service.update_status(
                id, Status.approved, user_id, background_tasks)

        return notify if notify else JSONResponse(None, status.HTTP_404_NOT_FOUND)

    @router.post("/notification/{id}/declined", tags=["notification"],
                 status_code=status.HTTP_200_OK)
    def declined(self,
    background_tasks: BackgroundTasks,
     id: int = Path("Notification ID"),
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

        notify = self.notify_service.update_status(id, Status.declined, user_id, background_tasks)
        return notify if notify else JSONResponse(None, status.HTTP_404_NOT_FOUND)

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
        user = self.user_service.get_detail_user_by_id(user_id)
        if not user:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED)

        total = self.notify_service.count_total_not_seen(user.work_for)

        return TotalNotSeenPayload(total=total)
