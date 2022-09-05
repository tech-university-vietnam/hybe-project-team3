from fastapi.testclient import TestClient
from fastapi import status

REGISTER_DATA = {"email": "test", "password": "123", "work_for": 1}
FAILED_REGISTER_DATA = {"email": "test", "password": "123"}
LOGIN_DATA = {"email": "test", "password": "123"}
FAILED_LOGIN_DATA = {"email": "test"}
REGISTER_PATH = "/register"
LOGIN_PATH = "/login"


def test_register_success(client: TestClient) -> None:
    r = client.post(
        REGISTER_PATH,
        json=REGISTER_DATA
    )
    assert r.status_code == status.HTTP_201_CREATED


def test_register_email_already_be_taken(client: TestClient) -> None:
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


def test_login_success(client: TestClient) -> None:
    r = client.post(
        LOGIN_PATH,
        json=LOGIN_DATA,
    )
    print(r.json())
    assert r.status_code == status.HTTP_200_OK
