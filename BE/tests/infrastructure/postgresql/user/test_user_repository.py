from tests import FunctionalTestCase

from app.domains.user import UserRepository
from app import inject
from app.controllers.user.auth_request import RegisterRequest


class TestUserRepository(FunctionalTestCase):
    @property
    def repo(self) -> UserRepository:
        return inject(UserRepository)

    def test_create(self):
        self.repo.create(RegisterRequest(email="paul@mckinsey.com",
                                         password="xx", work_for=1))
