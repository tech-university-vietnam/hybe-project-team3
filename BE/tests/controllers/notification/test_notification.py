from fastapi.testclient import TestClient
from fastapi import status

NOTI_PREFIX = "/notification"
SOURCE_DATA = {"name": "foo"}
LOGIN_DATA = {"email": "test2323", "password": "123"}
REGISTER_PATH = "/register"
LOGIN_PATH = "/login"

auth_header = {"Authorization": ""}
source_id = ""


def add_bearer(token: str):
    print(token)
    return f"Bearer {token}"


def test_get_token(client: TestClient) -> None:
    r = client.post(
        REGISTER_PATH,
        json={"email": "test2323", "password": "123", "work_for": 1}
    )
    r = client.post(
        LOGIN_PATH,
        json=LOGIN_DATA,
    )
    data = r.json()
    global auth_header
    auth_header["Authorization"] = add_bearer(data['token'])
    assert r.status_code == 200


def test_get_notseen_notification_quantity_first(client: TestClient) -> None:
    r = client.get(
        "notification/not-seen",
        headers=auth_header,
    )
    data = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert data['notseen_noti'] == 3


def test_get_notifications(client: TestClient) -> None:
    r = client.get(
        "notifications",
        headers=auth_header,
    )
    data = r.json()
    assert r.status_code == status.HTTP_200_OK
    for item in data:
        assert item['seenStatus'] == "seen"


def test_get_notseen_notification_quantity_after(client: TestClient) -> None:
    r = client.get(
        "notification/not-seen",
        headers=auth_header,
    )
    data = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert data['notseen_noti'] == 0


def test_approve_notification(client: TestClient) -> None:
    r = client.post(
        f"{NOTI_PREFIX}/{1}/approved",
        headers=auth_header,
        json={"id": 1}
    )
    data = r.json()
    assert r.status_code == status.HTTP_200_OK
    # assert data['status'] == "approved"


def test_declined_notification(client: TestClient) -> None:
    r = client.post(
        f"{NOTI_PREFIX}/{1}/declined",
        headers=auth_header,
    )
    data = r.json()
    assert r.status_code == status.HTTP_200_OK
    # assert data['status'] == "declined"
