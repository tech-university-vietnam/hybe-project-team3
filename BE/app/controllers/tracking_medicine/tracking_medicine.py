from typing import List

import pinject
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status

from app.controllers.tracking_medicine.model import TrackingMedicinePayload
from app.domains.medicine.medicine_service import MedicineService
from app.model.tracking_medicine import TrackingMedicine

router = InferringRouter()


@cbv(router)
class TrackingMedicineRoute:

    def __init__(self):
        obj_graph = pinject.new_object_graph()
        self.medicine_service: MedicineService = obj_graph.provide(MedicineService)

    @router.get("/tracking-medicines", tags=["medicine"], response_model=List[TrackingMedicine])
    def list_trackings(self):
        test = list(map(lambda m: m.dict(), self.medicine_service.list()))
        return JSONResponse(test)

    @router.get("/tracking-medicine/{tracking_id}", tags=["medicine"], response_model=TrackingMedicine)
    def get_tracking(self, tracking_id: int):
        medicine = self.medicine_service.get(tracking_id)
        return JSONResponse(medicine.dict())

    @router.post("/tracking-medicine", tags=["medicine"], response_model=TrackingMedicine)
    async def create_tracking_medicine(self, payload: TrackingMedicinePayload):
        medicine = self.medicine_service.create(payload)

        return JSONResponse(medicine.dict(), status.HTTP_201_CREATED)

    @router.put("/tracking-medicine/{tracking_id}", tags=["medicine"], response_model=TrackingMedicine)
    def update_tracking_medicine(self, tracking_id: int, payload: TrackingMedicinePayload):
        return self.medicine_service.update(tracking_id, payload)

    @router.delete("/tracking-medicine/{tracking_id}", tags=["medicine"], response_model=TrackingMedicine)
    def delete_tracking_medicine(self, tracking_id: int):
        success = self.medicine_service.delete(tracking_id)
        if success:
            return JSONResponse(None, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(None, status_code=status.HTTP_404_NOT_FOUND)


