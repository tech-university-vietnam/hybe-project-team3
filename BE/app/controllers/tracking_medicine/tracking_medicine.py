from typing import List

import pinject
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.controllers.tracking_medicine.model import TrackingMedicinePayload
from app.domains.medicine.medicine_service import MedicineService
from app.model.tracking_medicine import TrackingMedicine

router = InferringRouter()


@cbv(router)
class TrackingMedicineRoute:

    def __init__(self):
        obj_graph = pinject.new_object_graph()
        self.medicine_service: MedicineService = obj_graph.provide(MedicineService)

    @router.get("/tracking-medicines", tags=["medicine"], response_model=List[TrackingMedicinePayload])
    def list_trackings(self):
        return self.medicine_service.list()

    @router.get("/tracking-medicine/{tracking_id}", tags=["medicine"], response_model=TrackingMedicine)
    def get_tracking(self, tracking_id: int):
        return self.medicine_service.get(tracking_id)

    @router.post("/tracking-medicine", tags=["medicine"], response_model=TrackingMedicine)
    async def create_tracking_medicine(self, payload: TrackingMedicinePayload):
        medicine = self.medicine_service.create(payload)

        return medicine

    @router.put("/tracking-medicine/{tracking_id}", tags=["medicine"], response_model=TrackingMedicine)
    def update_tracking_medicine(self, tracking_id: int, payload: TrackingMedicinePayload):
        return self.medicine_service.update(tracking_id, payload)
