from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.controllers.auth.auth_request import RegisterRequest, LoginRequest
from app.domain.auth.auth_service import AuthService
from app.domain.auth.jwt_service import JWTService

router = InferringRouter()


@cbv(router)
class AuthenticationRoute:
    # Inject dependency services
    auth_service = AuthService()
    jwt_service = JWTService()

    @router.post("/login", tags=["authentication"])
    def login(self, login_req: LoginRequest):
        user = self.auth_service.login(**dict(login_req))
        if user:
            return {"token": self.jwt_service.encode(str(user.id))}
        return {"msg": "wrong email or password"}

    @router.post("/register", tags=["authentication"])
    def register(self, auth_req: RegisterRequest):
        return self.auth_service.register(auth_req)
