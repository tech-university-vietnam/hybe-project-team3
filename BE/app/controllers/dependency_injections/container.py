from typing import Type, TypeVar

from dependency_injector import containers, providers

from app.domains.helpers.database_repository import DatabaseRepository
from app.domains.hospital.hospital_repository import HospitalRepository
from app.domains.hospital.hostpital_service import HospitalService
from app.domains.medicine.medicine_repository import MedicineRepository
from app.domains.medicine.medicine_service import MedicineService
from app.domains.notification.notification_repository import NotificationRepository
from app.domains.notification.notification_service import NotificationService
from app.domains.source_order_request.source_order_request_repository import SourceOrderRequestRepository
from app.domains.source_order_request.source_order_request_service import SourceOrderRequestService
from app.domains.user.user_repository import UserRepository
from app.domains.user.user_service import UserService
from app.infrastructure.postgresql.database import SessionLocal
from app.services.auth_service import AuthService
from app.services.jwt_service import JWTService

T = TypeVar('T')


def singleton(cls: T) -> T:
    instance = [None]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper


@singleton
class Container(containers.DeclarativeContainer):
    database_repo_factory = providers.Factory(DatabaseRepository)
    session = providers.Singleton(SessionLocal)
    database_repo_factory.add_attributes(db=session)

    # repos
    user_repo_factory = providers.Factory(UserRepository, database_repository=database_repo_factory)
    notification_repo_factory = providers.Factory(NotificationRepository, database_repository=database_repo_factory)
    hospital_repo_factory = providers.Factory(HospitalRepository, database_repository=database_repo_factory)
    medicine_repo_factory = providers.Factory(MedicineRepository, database_repository=database_repo_factory)
    source_order_request_repo_factory = providers.Factory(SourceOrderRequestRepository,
                                                          database_repository=database_repo_factory)

    # services
    auth_service_factory = providers.Factory(
        AuthService,
        user_repository=user_repo_factory
    )
    jwt_service_factory = providers.Factory(
        JWTService,
        user_repository=user_repo_factory
    )
    user_service_factory = providers.Factory(
        UserService,
        user_repository=user_repo_factory
    )
    medicine_service_factory = providers.Factory(
        MedicineService,
        medicine_repository=medicine_repo_factory
    )
    hospital_service_factory = providers.Factory(
        HospitalService,
        hospital_repository=hospital_repo_factory
    )

    source_order_request_service_factory = providers.Factory(
        SourceOrderRequestService,
        source_order_req_repo=source_order_request_repo_factory
    )
    notification_service_factory = providers.Factory(
        NotificationService,
        notification_repository=notification_repo_factory,
        hospital_repository=hospital_repo_factory,
        medicine_repository=medicine_repo_factory,
        source_order_request_repository=source_order_request_repo_factory
    )
