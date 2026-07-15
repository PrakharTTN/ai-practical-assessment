import pytest


def test_login_success(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@admin.com", "password": "admin"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@admin.com", "password": "wrong"},
    )
    assert response.status_code == 401
    assert response.json()["error"] == "unauthorized"


def test_login_unknown_email(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "nobody@example.com", "password": "admin"},
    )
    assert response.status_code == 401


def test_protected_route_without_token(client):
    response = client.get("/api/tickets")
    assert response.status_code == 401
    assert response.json()["error"] == "unauthorized"


def test_protected_route_invalid_token(client):
    response = client.get(
        "/api/tickets",
        headers={"Authorization": "Bearer invalid.token.here"},
    )
    assert response.status_code == 401
