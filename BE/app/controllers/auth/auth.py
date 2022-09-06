import pinject
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.responses import JSONResponse

from app.controllers.user.auth_request import LogoutRequest, LoginRequest, RegisterRequest
from app.domains.user.user_service import UserService


from fastapi import HTTPException, status, Depends

from app.services.auth_service import AuthService
from app.services.jwt_service import JWTService

router = InferringRouter()


@cbv(router)
class AuthenticationRoute:

    def __init__(self):
        obj_graph = pinject.new_object_graph()

        self.auth_service = obj_graph.provide(AuthService)
        self.jwt_service = obj_graph.provide(JWTService)
        self.user_service = obj_graph.provide(UserService)

    @router.post("/login", tags=["authentication"])
    def login(self, login_req: LoginRequest):
        user = self.auth_service.login(**dict(login_req))
        if user:
            token: str = self.jwt_service.encode(str(user.id))
            if self.user_service.add_new_token(user.id, token):
                return {"token": token}
            else:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail="wrong email or password")

    @router.post("/register",
                 tags=["authentication"],
                 responses={422: {"description": "Email is already taken"}})
    def register(self, auth_req: RegisterRequest):
        if self.auth_service.register(auth_req):
            return JSONResponse(content={"msg": "Registered successully"},
                                status_code=201)
        else:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Email is already taken")

    @router.post("/logout",
                 tags=["authentication"],
                 responses={status.HTTP_401_UNAUTHORIZED:
                            {"description": "Missing bearer authorization"}})
    def logout(self, data: LogoutRequest,
               user_id: str = Depends(JWTService.validate_token)):
        if self.user_service.delete_token(user_id, data.email):
            return JSONResponse(content={"msg": "logged out successfully"},
                                status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
