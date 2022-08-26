from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.responses import JSONResponse
from app.controllers.auth.auth_request import LogoutRequest
from app.domain.user.user_service import UserService

from app.controllers.auth.auth_request import RegisterRequest, LoginRequest
from app.domain.auth.auth_service import AuthService
from app.domain.auth.jwt_service import JWTService
from fastapi import HTTPException, status, Depends
router = InferringRouter()


@cbv(router)
class AuthenticationRoute:
    # Inject dependency services
    auth_service = AuthService()
    jwt_service = JWTService()
    user_service = UserService()

    @router.post("/login", tags=["authentication"])
    def login(self, login_req: LoginRequest):
        user = self.auth_service.login(**dict(login_req))
        if (user):
            token: str = self.jwt_service.encode(user.id)
            if (self.user_service.add_new_token(user.id, token)):
                return {"token": token}
            else:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            raise HTTPException(404, detail="wrong email or password")

    @router.post("/register",
                 tags=["authentication"],
                 responses={422: {"description": "Email is already taken"}})
    def register(self, auth_req: RegisterRequest):
        if (self.auth_service.register(auth_req)):
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
               user_id: str = Depends(jwt_service.validate_token)):
        if (self.user_service.delete_token(user_id, data.email)):
            return JSONResponse(content={"msg": "logged out successfully"},
                                status_code=200)
        else:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
