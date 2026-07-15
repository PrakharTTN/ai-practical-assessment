import os

import pytest
from fastapi.testclient import TestClient

from app.main import app

DEFAULT_DATABASE_URL = "postgresql://ticket_user:changeme@localhost:5432/tickets_db"


@pytest.fixture(scope="session", autouse=True)
def set_database_url() -> None:
    os.environ.setdefault("DATABASE_URL", DEFAULT_DATABASE_URL)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def admin_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@admin.com", "password": "admin"},
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def agent_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/auth/login",
        json={"email": "agent@example.com", "password": "admin"},
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
