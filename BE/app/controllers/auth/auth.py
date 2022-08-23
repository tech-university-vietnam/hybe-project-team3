from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.controllers.auth.auth_request import RegisterRequest, LoginRequest
from app.domain.auth.auth_service import AuthService

router = InferringRouter()


@cbv(router)
class AuthenticationRoute:
    # Inject dependency services
    auth_service = AuthService()

    @router.post("/login", tags=["authentication"])
    def login(self, login_req: LoginRequest):
        return self.auth_service.login(**dict(login_req))

    @router.post("/register", tags=["authentication"])
    def register(self, auth_req: RegisterRequest):
        return self.auth_service.register(auth_req)
