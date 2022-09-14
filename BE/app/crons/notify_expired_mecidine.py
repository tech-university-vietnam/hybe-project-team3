from collections import defaultdict
from datetime import datetime, timedelta
from operator import and_
from typing import List

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from sqlalchemy import update

from app.controllers.dependency_injections.container import Container
from sqlalchemy import delete
from app.domains.helpers.database_repository import DatabaseRepository

from app.infrastructure.postgresql.tracking_medicine.tracking_medicine import TrackingMedicineDTO
from app.infrastructure.postgresql.notiffication.notification import NotificationDTO
from app.infrastructure.postgresql.source_order_request.source_order_request import SourceOrderRequestDTO


def setup_cron(app: FastAPI, debug=True):
    container = Container()
    db_repo: DatabaseRepository = container.database_repo

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

    def change_to_available_if_meds_sold_out(map_meds_hospital_sell):
        sources = db_repo.db.query(SourceOrderRequestDTO).filter(SourceOrderRequestDTO.status=="Available").all()
        source_ids_to_update = map(lambda source: source.id, filter(lambda source: source.name not in map_meds_hospital_sell.keys(), sources))
        mappings=[]
        for i in source_ids_to_update:
            stmt = (
                delete(NotificationDTO).
                where(NotificationDTO.sourcing_id == i,
                      NotificationDTO.sourcing_type == "source-order",
                      NotificationDTO.type == "notifyAvailable")
            )
            db_repo.db.execute(stmt)
            db_repo.db.commit()
            mappings.append({
                "id": i,
                "status": "Unavailable"
            })
        # update to availlable
        db_repo.db.bulk_update_mappings(SourceOrderRequestDTO, mappings)
        db_repo.db.commit()

        # update to availlable
    def check_available_meds():
        # Get the source-order unavailable (name and hospital_id)
        # Take the name and query the approved notification
        # if count >0 then create notification from hos to hos
        # create notis source-order
        # get listed med where name in source-order where status == unavailable
        # status == unavaiable and name in listed med
        # update source-order name where id in []
        meds: [TrackingMedicineDTO] = db_repo.db.query(TrackingMedicineDTO).filter(TrackingMedicineDTO.status=="Listed").all()
        map_meds_hospital_sell = defaultdict(list)
        for med in meds:
            map_meds_hospital_sell[med.name].append((med.hospital_id, med.id))

        sources = db_repo.db.query(SourceOrderRequestDTO).filter(SourceOrderRequestDTO.status=="Unavailable").all()
        map_meds_hospital_buy = defaultdict(list)
        source_ids_to_update = set(map(lambda source: source.id, filter(lambda source: source.name in map_meds_hospital_sell.keys(), sources)))
        change_to_available_if_meds_sold_out(map_meds_hospital_sell)
        # create update dict
        mappings = []
        for i in source_ids_to_update:
            mappings.append({
                "id": i,
                "status": "Available"
            })
        # update to availlable
        db_repo.db.bulk_update_mappings(SourceOrderRequestDTO, mappings)
        # db_repo.db.commit()
        for row in sources:
            # check if name in approved notification
            map_meds_hospital_buy[row.name].append((row.hospital_id, row.id))
        # join 2 list
        map_hospital_sell_buy = defaultdict(dict)
        for name in map_meds_hospital_sell.keys():
            map_hospital_sell_buy[name]['buyer'] = map_meds_hospital_buy[name]
            map_hospital_sell_buy[name]['seller'] = map_meds_hospital_sell[name]
        noti_list = []
        for name in map_hospital_sell_buy.keys():
            if (
                map_hospital_sell_buy[name]['seller']
                and
                map_hospital_sell_buy[name]['buyer']
            ):
                # 1 med can have multiple hospital_buyer
                for hospital_buy in map_hospital_sell_buy[name]['buyer']:
                    noti: NotificationDTO = NotificationDTO.from_sourcing_entity(
                        hospital_buy[1],
                        map_hospital_sell_buy[name]['seller'][0][1],
                        name,
                        map_hospital_sell_buy[name]['seller'][0][0],
                        hospital_buy[0]
                        )
                    noti_list += [noti]

        db_repo.db.add_all(noti_list)
        db_repo.db.commit()

    @app.on_event("startup")
    @repeat_every(seconds=30, raise_exceptions=True)  # 5 mins
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
        check_available_meds()

