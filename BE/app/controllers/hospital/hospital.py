from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class HospitalRoute:
    @router.get("/hospitals", tags=["hospitals"])
    def get_hospitals(self):
        dummy_hospitals = {
            "hospitals": [
                {
                    "id": 1,
                    "name": "foo1"
                },
                {
                    "id": 2,
                    "name": "foo2"
                },
                {
                    "id": 3,
                    "name": "foo3"
                },
                {
                    "id": 4,
                    "name": "foo4"
                },
                {
                    "id": 5,
                    "name": "foo5"
                }
            ]
        }
        return dummy_hospitals
