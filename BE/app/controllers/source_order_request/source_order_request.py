from fastapi_utils.cbv import cbv
from fastapi import Depends, HTTPException, status
from fastapi_utils.inferring_router import InferringRouter
from app.common.exceptions import DBError
from app.controllers.common.schema import CommonResponse
from app.controllers.dependency_injections.container import Container
from app.domains.user.user_service import UserService
from app.model.source_order_request import SourceOrderRequest, SourceOrderRequestPayload, SourceOrderRequestUpdatePayload
from app.services.jwt_service import JWTService
from app.domains.source_order_request.source_order_request_service import SourceOrderRequestService
from fastapi.security import HTTPAuthorizationCredentials
from app.main import oauth2_scheme

router = InferringRouter()


@cbv(router)
class SourceOrderRequestRoute:
    def __init__(self) -> None:
        container = Container()
        self.source_order_req_service: SourceOrderRequestService = container.source_order_request_service_factory()
        self.jwt_service: JWTService = container.jwt_service_factory()
        self.user_service: UserService = container.user_service_factory()

    @router.get("/source-orders", tags=["source-order"])
    def get_source_orders(self):
        try:
            return self.source_order_req_service.list()
        except DBError:
            raise HTTPException(500)

    @router.post("/source-order", tags=["source-order"],
                 status_code=status.HTTP_201_CREATED)
    def create_source_order(self, payload: SourceOrderRequestPayload,
                            bearer_auth: HTTPAuthorizationCredentials =
                            Depends(oauth2_scheme)) -> SourceOrderRequest:
        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401)
        try:
            payload.created_by = user.id
            payload.hospital_id = user.work_for
            source_order_req = self.source_order_req_service.create(payload)
            return source_order_req
        except DBError:
            raise HTTPException(500)

    @router.patch("/source-order/{source_id}", tags=["source-order"])
    def update_source_order(self, source_id: int,
                            payload: SourceOrderRequestUpdatePayload,
                            bearer_auth: HTTPAuthorizationCredentials =
                            Depends(oauth2_scheme)) -> CommonResponse:
        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401)
        try:
            self.source_order_req_service.update(payload, source_id, user_id)
            return {"msg": "updated"}
        except DBError:
            raise HTTPException(500)
        except PermissionError:
            raise HTTPException(500)

    @router.delete("/source-order/{source_id}", tags=["source-order"])
    def delete_source_order(self, source_id: int,
                            bearer_auth: HTTPAuthorizationCredentials =
                            Depends(oauth2_scheme)) -> CommonResponse:
        user_id = self.jwt_service.validate_token(bearer_auth.credentials)
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401)
        try:
            self.source_order_req_service.delete(source_id, user_id)
            return {"msg": "ok"}
        except DBError:
            raise HTTPException(500)
        except PermissionError:
            raise HTTPException(500)
