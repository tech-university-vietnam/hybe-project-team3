from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class UserRoute:
    # Inject dependency services

    @router.get("/users/me", tags=["users"])
    async def get_current_user(self):
        return {"username": "fakecurrentuser"}

    @router.get("/users/{username}", tags=["users"])
    async def get_user(self, username: str):
        return {"username": username}
