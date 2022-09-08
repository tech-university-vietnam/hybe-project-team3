from fastapi.testclient import TestClient
from fastapi import status

SOURCE_ORDER_PREFIX = "/source-order"
SOURCE_DATA = {"name": "foo"}
LOGIN_DATA = {"email": "test23", "password": "123"}
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
        json={"email": "test23", "password": "123", "work_for":1}
    )
    r = client.post(
        LOGIN_PATH,
        json=LOGIN_DATA,
    )
    data = r.json()
    global auth_header
    auth_header["Authorization"] = add_bearer(data['token'])
    assert r.status_code == 200


def test_create_source_order(client: TestClient) -> None:
    r = client.post(
        SOURCE_ORDER_PREFIX,
        headers=auth_header,
        json={"name": "foo"}
    )
    data = r.json()
    assert r.status_code == status.HTTP_201_CREATED
    assert data['name'] == "foo"


def test_get_source_order_list(client: TestClient) -> None:
    r = client.get(
        "/source-orders",
        headers=auth_header
    )
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert data[0]['name'] == "foo"
    global source_id
    source_id = data[0]['id']


def test_update_source_order(client: TestClient) -> None:
    r = client.patch(
        f'{SOURCE_ORDER_PREFIX}/{source_id}',
        headers=auth_header,
        json={"status": "foo2"}
    )
    assert r.status_code == status.HTTP_200_OK
    r = client.get(
        "/source-orders",
    )
    data = r.json()
    assert data[0]['status'] == "foo2"


def test_delete_source_order(client: TestClient) -> None:
    r = client.delete(
        f'{SOURCE_ORDER_PREFIX}/{source_id}',
        headers=auth_header,
    )
    assert r.status_code == status.HTTP_200_OK
    r = client.get(
        "/source-orders",
    )
    data = r.json()
    assert data == []
