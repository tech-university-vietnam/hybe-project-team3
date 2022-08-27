from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.responses import JSONResponse
from app.controllers.auth.auth_request import LogoutRequest
from app.domain.user.user_service import UserService
from sqlalchemy.orm import Session
from app.controllers.auth.auth_request import RegisterRequest, LoginRequest
from app.domain.auth.auth_service import AuthService
from app.domain.auth.jwt_service import JWTService
from fastapi import HTTPException, status, Depends
from app import deps
router = InferringRouter()


@cbv(router)
class AuthenticationRoute:
    # Inject dependency services
    auth_service = AuthService()
    jwt_service = JWTService()
    user_service = UserService()

    @router.post("/login", tags=["authentication"])
    def login(self, login_req: LoginRequest,
              db: Session = Depends(deps.get_db)):
        user = self.auth_service.login(login_req.email, login_req.password, db)
        if user:
            token: str = self.jwt_service.encode(str(user.id))
            if (self.user_service.add_new_token(user.id, token, db)):
                return {"token": token}
            else:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail="wrong email or password")

    @router.post("/register",
                 tags=["authentication"],
                 responses={status.HTTP_422_UNPROCESSABLE_ENTITY:
                            {"description": "Email is already taken"}})
    def register(self, auth_req: RegisterRequest,
                 db: Session = Depends(deps.get_db)):
        if (self.auth_service.register(auth_req, db)):
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
               user_id: str = Depends(jwt_service.validate_token),
               db: Session = Depends(deps.get_db)):
        if (self.user_service.delete_token(user_id, data.email, db)):
            return JSONResponse(content={"msg": "logged out successfully"},
                                status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
