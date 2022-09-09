from fastapi.testclient import TestClient
from fastapi import status
TRACKING_MEDICINE_PREFIX = "/tracking-medicine"
TRACKING_DATA = {"name": "foo"}
LOGIN_DATA = {"email": "test23", "password": "123"}
REGISTER_PATH = "/register"
LOGIN_PATH = "/login"

auth_header = {"Authorization": ""}
medicine_id = ""


def add_bearer(token: str):
    return f"Bearer {token}"


def test_get_token(client: TestClient) -> None:
    r = client.post(
        REGISTER_PATH,
        json={"email": "test12323", "password": "123", "work_for": 1}
    )
    r = client.post(
        LOGIN_PATH,
        json=LOGIN_DATA,
    )
    data = r.json()
    global auth_header
    auth_header["Authorization"] = add_bearer(data['token'])
    assert r.status_code == 200


def test_create_tracking_medicine(client: TestClient) -> None:
    r = client.post(
        TRACKING_MEDICINE_PREFIX,
        headers=auth_header,
        json={"name": "foo", "expired_date": "2022-09-07T13:00:50.280Z"}
    )
    assert r.status_code == status.HTTP_201_CREATED
    data = r.json()
    assert data['name'] == "foo"


def test_get_tracking_medicine_list(client: TestClient) -> None:
    r = client.get(
        "/tracking-medicines",
        headers=auth_header
    )
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert data[0]['name'] == "foo"
    global medicine_id
    medicine_id = data[0]['id']


def test_update_tracking_medicine(client: TestClient) -> None:
    r = client.put(
        f'{TRACKING_MEDICINE_PREFIX}/{medicine_id}',
        headers=auth_header,
        json={"name": "foo2", "expired_date": "2022-09-07T13:00:50.280Z",
              "status": "bar", "created_by": 1, "hospital_id": 1}
    )
    assert r.status_code == status.HTTP_200_OK
    r = client.get(
        "/tracking-medicines",
    )
    data = r.json()
    assert data[0]['name'] == "foo2"


def test_delete_tracking_medicine(client: TestClient) -> None:
    r = client.delete(
        f'{TRACKING_MEDICINE_PREFIX}/{medicine_id}',
        headers=auth_header,
    )
    assert r.status_code == status.HTTP_200_OK
    r = client.get(
        "/tracking-medicines",
    )
    data = r.json()
    assert data[0]['name'] != "foo"
