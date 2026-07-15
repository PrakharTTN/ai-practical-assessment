from tests.backend.helpers import create_ticket


def test_list_tickets_authenticated(client, admin_headers):
    response = client.get("/api/tickets", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_create_ticket_success(client, admin_headers):
    response = client.post(
        "/api/tickets",
        headers=admin_headers,
        json={
            "title": "Integration test ticket",
            "description": "Created by pytest",
            "priority": "high",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Integration test ticket"
    assert data["status"] == "open"
    assert data["created_by"]["email"] == "admin@admin.com"


def test_create_ticket_missing_title(client, admin_headers):
    response = client.post(
        "/api/tickets",
        headers=admin_headers,
        json={"description": "No title", "priority": "low"},
    )
    assert response.status_code == 422
    assert response.json()["error"] == "validation_error"
    assert "title" in response.json()["details"]


def test_get_ticket_detail(client, admin_headers):
    created = create_ticket(client, admin_headers, title="Detail test")
    response = client.get(f"/api/tickets/{created['id']}", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert "comments" in data


def test_get_ticket_not_found(client, admin_headers):
    response = client.get("/api/tickets/999999", headers=admin_headers)
    assert response.status_code == 404
    assert response.json()["error"] == "not_found"


def test_update_ticket_fields(client, admin_headers, agent_headers):
    created = create_ticket(client, admin_headers, title="Before update")
    response = client.patch(
        f"/api/tickets/{created['id']}",
        headers=admin_headers,
        json={
            "title": "After update",
            "priority": "low",
            "assigned_to_id": 2,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "After update"
    assert data["priority"] == "low"
    assert data["assigned_to"]["email"] == "agent@example.com"


def test_update_ticket_cannot_change_status(client, admin_headers):
    created = create_ticket(client, admin_headers)
    response = client.patch(
        f"/api/tickets/{created['id']}",
        headers=admin_headers,
        json={"title": "Still open"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "open"


def test_add_comment(client, admin_headers):
    created = create_ticket(client, admin_headers)
    response = client.post(
        f"/api/tickets/{created['id']}/comments",
        headers=admin_headers,
        json={"message": "pytest comment"},
    )
    assert response.status_code == 201
    assert response.json()["message"] == "pytest comment"

    detail = client.get(f"/api/tickets/{created['id']}", headers=admin_headers)
    assert any(c["message"] == "pytest comment" for c in detail.json()["comments"])


def test_add_comment_empty_message(client, admin_headers):
    created = create_ticket(client, admin_headers)
    response = client.post(
        f"/api/tickets/{created['id']}/comments",
        headers=admin_headers,
        json={"message": ""},
    )
    assert response.status_code == 422


def test_filter_by_status(client, admin_headers):
    create_ticket(client, admin_headers, title="Filter open ticket")
    response = client.get(
        "/api/tickets",
        headers=admin_headers,
        params={"status": "open"},
    )
    assert response.status_code == 200
    assert all(t["status"] == "open" for t in response.json())


def test_search_by_title(client, admin_headers):
    create_ticket(client, admin_headers, title="UniqueSearchTermXYZ")
    response = client.get(
        "/api/tickets",
        headers=admin_headers,
        params={"search": "UniqueSearchTermXYZ"},
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert any("UniqueSearchTermXYZ" in t["title"] for t in response.json())
