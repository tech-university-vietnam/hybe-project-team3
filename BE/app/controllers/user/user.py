import pinject
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import HTTPException, status, Header
from fastapi.responses import JSONResponse
from app.controllers.user.schema import LoginResponse

from app.controllers.user.auth_request import (
    LoginRequest, RegisterRequest, LogoutRequest)
from app.services.auth_service import AuthService
from app.services.jwt_service import JWTService
from app.domains.user.user_service import UserService
from app.controllers.common.schema import CommonResponse
router = InferringRouter()


@cbv(router)
class UserRoute:
    def __init__(self):
        obj_graph = pinject.new_object_graph()
        self.auth_service: AuthService = obj_graph.provide(AuthService)
        self.jwt_service: JWTService = obj_graph.provide(JWTService)
        self.user_service: UserService = obj_graph.provide(UserService)

    @router.post("/login", tags=["users"])
    def login(self, login_req: LoginRequest) -> LoginResponse:
        user = self.auth_service.login(**dict(login_req))
        if user:
            token: str = self.jwt_service.encode(str(user.id))
            if self.user_service.add_new_token(user.id, token):
                return {"token": token}
            else:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            raise HTTPException(404, detail="wrong email or password")

    @router.post("/register",
                 tags=["authentication"],
                 responses={422: {"description": "Email is already taken"}})
    def register(self, auth_req: RegisterRequest) -> CommonResponse:
        if self.auth_service.register(auth_req):
            return JSONResponse(content={"msg": "Registered successully"},
                                status_code=201)
        else:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Email is already taken")

    @router.post("/logout",
                 tags=["authentication"],
                 responses={
                     401: {"description": "Missing bearer authorization"}})
    def logout(self, data: LogoutRequest,
               authorization=Header()) -> CommonResponse:
        user_id = self.jwt_service.validate_token(authorization)
        if self.user_service.delete_token(user_id, data.email):
            return JSONResponse(content={"msg": "logged out successfully"},
                                status_code=200)
        else:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @router.get("/user", tags=["users"])
    async def get_user(self,
                       authorization: str = Header()):
        user_id = self.jwt_service.validate_token(authorization)
        user = self.user_service.get_user_by_id(user_id)
        return user
