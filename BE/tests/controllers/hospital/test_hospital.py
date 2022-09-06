from fastapi.testclient import TestClient
from fastapi import status


def test_seed_hospital(client: TestClient) -> None:
    r = client.get(
        "/hospitals/seed",
    )
    assert r.status_code == status.HTTP_201_CREATED


def test_get_hospital(client: TestClient) -> None:
    r = client.get(
        "/hospitals/seed",
    )
    assert r.status_code == status.HTTP_201_CREATED
