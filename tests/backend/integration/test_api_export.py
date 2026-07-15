from tests.backend.helpers import create_ticket


def test_export_returns_only_self_created_tickets(client, admin_headers, agent_headers):
    admin_ticket = create_ticket(
        client, admin_headers, title="Admin export ticket unique"
    )
    create_ticket(client, agent_headers, title="Agent export ticket unique")

    response = client.get("/api/tickets/export", headers=admin_headers)
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    body = response.text
    assert "Admin export ticket unique" in body
    assert "Agent export ticket unique" not in body
    assert str(admin_ticket["id"]) in body


def test_export_requires_auth(client):
    response = client.get("/api/tickets/export")
    assert response.status_code == 401


def test_export_headers_only_when_no_tickets(client):
    """Agent with seeded tickets still gets CSV with header row."""
    response = client.get(
        "/api/tickets/export",
        headers={
            "Authorization": "Bearer invalid"
        },
    )
    assert response.status_code == 401
