"""User management API tests."""

import uuid


def test_list_users_requires_auth(client):
    response = client.get("/api/users")
    assert response.status_code == 401


def test_list_users_as_admin(client, admin_headers):
    response = client.get("/api/users", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert all("email" in u and "password" not in str(u) for u in data)


def test_get_me_returns_current_user(client, admin_headers):
    response = client.get("/api/auth/me", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@admin.com"
    assert data["role"] == "admin"


def test_get_me_requires_auth(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_admin_can_create_user(client, admin_headers):
    email = f"support-{uuid.uuid4().hex[:8]}@example.com"
    response = client.post(
        "/api/users",
        headers=admin_headers,
        json={
            "name": "New Support Agent",
            "email": email,
            "password": "secure1",
            "role": "agent",
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == email
    assert data["role"] == "agent"
    assert "password" not in data

    login = client.post(
        "/api/auth/login",
        json={"email": email, "password": "secure1"},
    )
    assert login.status_code == 200


def test_agent_cannot_create_user(client, agent_headers):
    response = client.post(
        "/api/users",
        headers=agent_headers,
        json={
            "name": "Blocked User",
            "email": f"blocked-{uuid.uuid4().hex[:8]}@example.com",
            "password": "secure1",
            "role": "agent",
        },
    )
    assert response.status_code == 403
    assert response.json()["error"] == "forbidden"


def test_create_user_duplicate_email(client, admin_headers):
    response = client.post(
        "/api/users",
        headers=admin_headers,
        json={
            "name": "Duplicate",
            "email": "admin@admin.com",
            "password": "secure1",
            "role": "agent",
        },
    )
    assert response.status_code == 409
    assert response.json()["error"] == "duplicate_email"


def test_create_user_validation(client, admin_headers):
    response = client.post(
        "/api/users",
        headers=admin_headers,
        json={
            "name": "",
            "email": "not-an-email",
            "password": "x",
            "role": "agent",
        },
    )
    assert response.status_code == 422


def test_admin_can_update_user(client, admin_headers):
    email = f"edit-{uuid.uuid4().hex[:8]}@example.com"
    create = client.post(
        "/api/users",
        headers=admin_headers,
        json={
            "name": "Before Edit",
            "email": email,
            "password": "secure1",
            "role": "agent",
        },
    )
    user_id = create.json()["id"]

    response = client.patch(
        f"/api/users/{user_id}",
        headers=admin_headers,
        json={
            "name": "After Edit",
            "role": "admin",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "After Edit"
    assert data["role"] == "admin"
    assert data["email"] == email


def test_admin_can_update_user_password(client, admin_headers):
    email = f"pwd-{uuid.uuid4().hex[:8]}@example.com"
    create = client.post(
        "/api/users",
        headers=admin_headers,
        json={
            "name": "Password User",
            "email": email,
            "password": "oldpass1",
            "role": "agent",
        },
    )
    user_id = create.json()["id"]

    response = client.patch(
        f"/api/users/{user_id}",
        headers=admin_headers,
        json={"password": "newpass1"},
    )
    assert response.status_code == 200

    old_login = client.post(
        "/api/auth/login",
        json={"email": email, "password": "oldpass1"},
    )
    assert old_login.status_code == 401

    new_login = client.post(
        "/api/auth/login",
        json={"email": email, "password": "newpass1"},
    )
    assert new_login.status_code == 200


def test_agent_cannot_update_user(client, agent_headers, admin_headers):
    users = client.get("/api/users", headers=admin_headers).json()
    target_id = users[0]["id"]

    response = client.patch(
        f"/api/users/{target_id}",
        headers=agent_headers,
        json={"name": "Blocked Edit"},
    )
    assert response.status_code == 403


def test_update_user_not_found(client, admin_headers):
    response = client.patch(
        "/api/users/999999",
        headers=admin_headers,
        json={"name": "Missing"},
    )
    assert response.status_code == 404


def test_update_user_duplicate_email(client, admin_headers):
    users = client.get("/api/users", headers=admin_headers).json()
    agent = next(u for u in users if u["email"] == "agent@example.com")

    response = client.patch(
        f"/api/users/{agent['id']}",
        headers=admin_headers,
        json={"email": "admin@admin.com"},
    )
    assert response.status_code == 409
    assert response.json()["error"] == "duplicate_email"
