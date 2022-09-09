from datetime import datetime, timedelta
from operator import and_
from typing import List

import pinject
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from sqlalchemy import update

from app.domains.helpers.database_repository import DatabaseRepository

from app.infrastructure.postgresql.tracking_medicine.tracking_medicine import TrackingMedicineDTO
from app.infrastructure.postgresql.notiffication.notification import NotificationDTO


def setup_cron(app: FastAPI, debug=False):
    obj_graph = pinject.new_object_graph()
    db_repo: DatabaseRepository = obj_graph.provide(DatabaseRepository)

    def check_expired_meds(meds: [TrackingMedicineDTO]):
        utc_now = datetime.utcnow()
        expired_meds = list(map(lambda med: med.id, filter(lambda med: med.expired_date < utc_now, meds)))
        # Update the status to expired, save to db
        if not expired_meds:
            return

        if debug:
            print("%s records found expired: %s" % (len(expired_meds), expired_meds))

        stmt = (
            update(TrackingMedicineDTO).
            values(status='Expired').
            where(TrackingMedicineDTO.id.in_(expired_meds))
        )
        db_repo.db.execute(stmt)
        db_repo.db.commit()

    def check_nearly_expired_meds(meds: [TrackingMedicineDTO]):
        utc_now = datetime.utcnow()

        # Get meds need create noti
        near_expired_meds: [TrackingMedicineDTO] = list(filter(
            lambda med: utc_now >= (med.expired_date - timedelta(days=60)), meds))
        near_expired_med_ids = map(lambda med: med.id, near_expired_meds)

        if debug:
            near_expired_med_ids = list(near_expired_med_ids)
            print("%s meds in near_expired_meds" % len(near_expired_med_ids))

        # Get noti already created
        created_notis = db_repo.db.query(NotificationDTO). \
            where(and_(NotificationDTO.sourcing_type == 'tracking',
                       NotificationDTO.sourcing_id.in_(list(near_expired_med_ids)))).all()
        created_noti_source_ids = set(map(lambda noti: noti.sourcing_id, created_notis))

        if debug:
            print("Set created noti: ", created_noti_source_ids)

        # Exclude med existed in noti
        meds_to_create_noti: [TrackingMedicineDTO] = filter(lambda med: med.id not in created_noti_source_ids,
                                                            near_expired_meds)

        if debug:
            meds_to_create_noti = list(meds_to_create_noti)
            print("%s records in meds_to_create_noti: %s" % (len(meds_to_create_noti), meds_to_create_noti))

        noti_list = []
        for med in meds_to_create_noti:
            noti: NotificationDTO = NotificationDTO.from_tracking_medicine(med)
            noti_list += [noti]

        db_repo.db.add_all(noti_list)
        db_repo.db.commit()

    def check_available_meds(meds: [NotificationDTO]):
        # Get the listed med name
        # create notis source-order

        near_e: [NotificationDTO] = list(filter(
            lambda med: med.status == "List", meds))
        available_med_ids = map(lambda med: med.id, available_meds)

        if debug:
            available_med_ids = list(available_med_ids)
            print("%s meds in available_meds" % len(available_med_ids))

        created_notis = db_repo.db.query(NotificationDTO). \
            where(and_(NotificationDTO.sourcing_type == 'source-order',
                       NotificationDTO.in_(list(available_med_ids)))).all()
        created_noti_source_ids = set(map(lambda noti: noti.sourcing_id, created_notis))

        if debug:
            print("Set created noti: ", created_noti_source_ids)

        # Exclude med existed in noti
        meds_to_create_noti: [TrackingMedicineDTO] = filter(lambda med: med.id not in created_noti_source_ids,
                                                            available_meds)

        if debug:
            meds_to_create_noti = list(meds_to_create_noti)
            print("%s records in meds_to_create_noti: %s" % (len(meds_to_create_noti), meds_to_create_noti))

        noti_list = []
        for med in meds_to_create_noti:
            noti: NotificationDTO = NotificationDTO.from_tracking_medicine(med)
            noti_list += [noti]

        db_repo.db.add_all(noti_list)
        db_repo.db.commit()

    @app.on_event("startup")
    @repeat_every(seconds=60 * 5)  # 5 mins
    def notify_expired_medicine() -> None:
        print("Starting cronjob interval...")
        # Send nearly expired noti to owner
        med_dtos: List[TrackingMedicineDTO] = db_repo.db.query(TrackingMedicineDTO).where(
            TrackingMedicineDTO.status.in_(['Not listed', 'Listing'])).all()

        not_listing_meds = filter(lambda med: med.status == 'Not listed', med_dtos)

        if debug:
            not_listing_meds = list(not_listing_meds)
            print('not_listing_meds: %s records', len(not_listing_meds))

        # Update status to expired
        check_expired_meds(med_dtos)

        # Create noti for owner if med reaches near-expired date
        check_nearly_expired_meds(not_listing_meds)
