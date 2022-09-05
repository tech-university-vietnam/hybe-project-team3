import pytest
from fastapi.testclient import TestClient
# # Import the SQLAlchemy parts
from app.main import app


@pytest.fixture()
def client():
    yield TestClient(app)
