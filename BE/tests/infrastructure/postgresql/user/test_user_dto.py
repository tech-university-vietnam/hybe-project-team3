from app.controllers.auth.auth_request import RegisterRequest

from app.infrastructure.postgresql.user.user_dto import UserDTO
from datetime import datetime

from app.model.user import User
import bcrypt

now = datetime.now()


class TestUserDTO:
    def test_to_entity_model_should_create_entity_instance(self):
        user_dto = UserDTO(
            id=1,
            username="foo",
            email="foo@gmail.com",
            address="foooo",
            telephone="1",
            avatar="foo/bar",
            work_for=1,
            created_at=now,
            updated_at=now,
        )

        user = user_dto.to_entity()

        assert user.username == "foo"
        assert user.email == "foo@gmail.com"

        assert user.telephone == "1"
        assert user.work_for == 1

        assert user.created_at == now
        assert user.updated_at == now

    def test_from_entity_should_create_dto_instance(self):
        user = User(
            id=1,
            username="foo",
            email="foo@gmail.com",
            address="foooo",
            telephone="1",
            avatar="foo/bar",
            work_for=1
        )

        user_dto = UserDTO.from_entity(user)

        assert user.id == 1
        assert (
            user_dto.username
            == "foo"
        )
        assert (
            user_dto.email
            == "foo@gmail.com"
        )
        assert (
            user_dto.telephone
            == "1"
        )
        assert user_dto.work_for == 1
        assert isinstance(user_dto.created_at, datetime)
        assert isinstance(user_dto.updated_at, datetime)

    def test_from_register_request_should_create_dto_instance(self):
        register_request = RegisterRequest(
            password="123",
            email="foo@gmail.com",
            work_for=1
        )

        user_dto = UserDTO.from_register_request(register_request)

        assert (
            user_dto.email
            == "foo@gmail.com"
        )
        password = register_request.password.encode('utf8')
        hash_pw = user_dto.hash_pw.encode('utf8')

        assert bcrypt.checkpw(password, hash_pw)
        assert user_dto.work_for == 1
        assert isinstance(user_dto.created_at, datetime)
        assert isinstance(user_dto.updated_at, datetime)
