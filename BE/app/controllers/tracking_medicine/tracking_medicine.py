import logging
from datetime import datetime
from typing import List

import pinject
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.controllers.tracking_medicine.model import TrackingMedicinePayload
from app.domains.medicine.medicine_service import MedicalService
from app.model.tracking_medicine import TrackingMedicine

router = InferringRouter()


def dummy_tracking_medicine(index: int) -> TrackingMedicinePayload:
    return TrackingMedicinePayload(
        name="name-%s" % index,
        number=index,
        status='init',
        buy_price=0.0,
        manufacturer=index,
        expired_date=datetime.now(),
        created_at=datetime.now(),
        created_by=index,
        image="Base64 encoded image",
        hospital_id=index,
    )


DUMMY_MEDICINES = list(map(dummy_tracking_medicine, range(100)))


@cbv(router)
class TrackingMedicineRoute:

    def __init__(self):
        obj_graph = pinject.new_object_graph()
        self.medicine_service: MedicalService = obj_graph.provide(MedicalService)

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
