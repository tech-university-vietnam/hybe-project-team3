from fastapi.testclient import TestClient
from fastapi import status

SOURCE_ORDER_PREFIX = "/source-order"
SOURCE_DATA = {"name": "foo"}
LOGIN_DATA = {"email": "test23", "password": "123"}
FAILED_LOGIN_DATA = {"email": "test"}
REGISTER_PATH = "/register"
LOGIN_PATH = "/login"
GET_USER_PATH = '/user'

auth_header = {"Authorization": "Bearer"}
source_id = ""


def add_bearer(token: str):
    return f"Bearer {token}"

def test_register_success(client: TestClient) -> None:
    r = client.post(
        REGISTER_PATH,
        json={"email": "test23", "password": "123", "work_for":1}
    )
    assert r.status_code == status.HTTP_201_CREATED

def get_token(client: TestClient) -> None:
    r = client.post(
        LOGIN_PATH,
        json=LOGIN_DATA,
    )
    data = r.json()
    auth_header["Authorization"] = add_bearer(data['token'])


def test_create_source_order(client: TestClient) -> None:
    r = client.post(
        SOURCE_ORDER_PREFIX,
        headers=auth_header,
        json={"name": "foo"}
    )
    assert r.status_code == status.HTTP_201_CREATED
    assert r.json().name == "foo"


def test_get_source_order_list(client: TestClient) -> None:
    r = client.get(
        "/source-orders",
        headers=auth_header
    )
    assert r.status_code == status.HTTP_201_CREATED
    data = r.json()
    assert data[0]['name'] == "foo"
    global source_id
    source_id = data[0]['id']


def test_update_source_order(client: TestClient) -> None:
    r = client.patch(
        SOURCE_ORDER_PREFIX + "/" + source_id,
        headers=auth_header,
        json={"name": "foo2"}
    )
    assert r.status_code == status.HTTP_200_OK
    r = client.get(
        "/source-orders",
    )
    data =  r.json()
    assert data[0].name == "foo2"


def test_delete_source_order(client: TestClient) -> None:
    r = client.delete(
        SOURCE_ORDER_PREFIX + "/" + source_id,
        headers=auth_header,
    )
    assert r.status_code == status.HTTP_200_OK
    r = client.get(
        "/source-orders",
    )
    data = r.json()
    assert data == []


# def test_login_failed(client: TestClient) -> None:
#     r = client.post(
#         LOGIN_PATH,
#         json=FAILED_LOGIN_DATA,
#     )
#     assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY





# def test_get_user(client: TestClient) -> None:
#     r = client.get(
#         "/user",
#         headers=auth_header,
#     )
#     assert r.status_code == status.HTTP_200_OK
#     data = r.json()
#     assert "username" in data
#     assert "email" in data
#     assert "work_for" in data
#     assert "created_at" in data
#     assert "updated_at" in data


# def test_logout_missing_auth_header(client: TestClient) -> None:
#     r = client.post(
#         "/logout",
#         json={"email": "test"}
#     )
#     assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# def test_logout_success(client: TestClient) -> None:
#     r = client.post(
#         "/logout",
#         headers=auth_header,
#         json={"email": "test"}
#     )
#     assert r.status_code == status.HTTP_200_OK


# def test_get_user_missing_auth(client: TestClient) -> None:
#     r = client.get(
#         "/user",
#     )
#     assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# def test_get_user_invalidated_token(client: TestClient) -> None:
#     r = client.get(
#         "/user",
#         headers=auth_header,
#     )
#     assert r.status_code == status.HTTP_401_UNAUTHORIZED
