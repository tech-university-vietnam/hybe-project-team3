from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.domain.user.user_service import UserService

router = InferringRouter()


@cbv(router)
class UserRoute:
    # Inject dependency services
    user_service = UserService

    @router.get("/users/me", tags=["users"])
    async def get_current_user(self):
        return {"username": "fakecurrentuser"}

    @router.get("/users/{username}", tags=["users"])
    async def get_user(self, username: str):
        return {"username": username}
