from fastapi.testclient import TestClient
from fastapi import status
import pytest
from app.domains.user.user_exception import EmailAlreadyRegisteredError, EmailNotFoundError

REGISTER_DATA = {"email": "test", "password": "123", "work_for": 1}
FAILED_REGISTER_DATA = {"email": "test", "password": "123"}
LOGIN_DATA = {"email": "test", "password": "123"}
FAILED_LOGIN_DATA = {"email": "test"}
REGISTER_PATH = "/register"
LOGIN_PATH = "/login"
GET_USER_PATH = '/user'

auth_header = {"Authorization": "Bearer"}


def add_bearer(token: str):
    return f"Bearer {token}"


def test_register_success(client: TestClient) -> None:
    r = client.post(
        REGISTER_PATH,
        json=REGISTER_DATA
    )
    assert r.status_code == status.HTTP_201_CREATED


def test_register_email_already_be_taken(client: TestClient) -> None:
    with pytest.raises(EmailAlreadyRegisteredError):
        r = client.post(
            REGISTER_PATH,
            json=REGISTER_DATA
        )
        assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_register_validation_error(client: TestClient) -> None:
    r = client.post(
        REGISTER_PATH,
        json=FAILED_REGISTER_DATA
    )
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_failed(client: TestClient) -> None:
    r = client.post(
        LOGIN_PATH,
        json=FAILED_LOGIN_DATA,
    )
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_email_not_found(client: TestClient) -> None:
    r = client.post(
        LOGIN_PATH,
        json={"email": "foo", "password": "123", "work_for": 1}
    )
    assert r.status_code == status.HTTP_404_NOT_FOUND


def test_login_success(client: TestClient) -> None:
    r = client.post(
        LOGIN_PATH,
        json=LOGIN_DATA,
    )
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    auth_header["Authorization"] = add_bearer(data['token'])


def test_get_user(client: TestClient) -> None:
    r = client.get(
        "/user",
        headers=auth_header,
    )
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert "username" in data
    assert "email" in data
    assert "work_for" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_logout_missing_auth_header(client: TestClient) -> None:
    r = client.post(
        "/logout",
        json={"email": "test"}
    )
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_logout_success(client: TestClient) -> None:
    r = client.post(
        "/logout",
        headers=auth_header,
        json={"email": "test"}
    )
    assert r.status_code == status.HTTP_200_OK


def test_get_user_missing_auth(client: TestClient) -> None:
    r = client.get(
        "/user",
    )
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_get_user_invalidated_token(client: TestClient) -> None:
    r = client.get(
        "/user",
        headers=auth_header,
    )
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
