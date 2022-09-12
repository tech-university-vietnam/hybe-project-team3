from fastapi.testclient import TestClient
from fastapi import status


def test_get_hospital(client: TestClient) -> None:
    r = client.get(
        "/hospitals",
    )
    data = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert data != []
    assert 'name' in data[0]
