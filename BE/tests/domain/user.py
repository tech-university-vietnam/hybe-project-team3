
from app.model.user import User
from datetime import datetime

now = datetime.utcnow()


class TestUserModel:
    def test_constructor_should_create_instance(self):
        user = User(
            id=1,
            username="foo",
            email="foo@gmail.com",
            telephone="1",
            hash_pw="asdas",
            token="das",
            avatar="foo/bar",
            work_for=1
        )

        assert user.username == "foo"
        assert user.email == "foo@gmail.com"
        assert user.hash_pw == "asdas"
        assert user.token == "das"

        assert user.telephone == "1"
        assert user.work_for == 1
        assert user.created_at == now
        assert user.updated_at == now
