import pytest

from tests.backend.helpers import create_ticket, ticket_in_status, transition_status


@pytest.mark.parametrize(
    ("target_status",),
    [
        ("in_progress",),
        ("cancelled",),
    ],
)
def test_valid_transitions_from_open(client, admin_headers, target_status):
    ticket = create_ticket(client, admin_headers, title=f"Open to {target_status}")
    response = transition_status(client, admin_headers, ticket["id"], target_status)
    assert response.status_code == 200
    assert response.json()["status"] == target_status


def test_valid_transition_in_progress_to_resolved(client, admin_headers):
    ticket = ticket_in_status(client, admin_headers, "in_progress")
    response = transition_status(client, admin_headers, ticket["id"], "resolved")
    assert response.status_code == 200
    assert response.json()["status"] == "resolved"


def test_valid_transition_in_progress_to_cancelled(client, admin_headers):
    ticket = ticket_in_status(client, admin_headers, "in_progress")
    response = transition_status(client, admin_headers, ticket["id"], "cancelled")
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"


def test_valid_transition_resolved_to_closed(client, admin_headers):
    ticket = ticket_in_status(client, admin_headers, "resolved")
    response = transition_status(client, admin_headers, ticket["id"], "closed")
    assert response.status_code == 200
    assert response.json()["status"] == "closed"


@pytest.mark.parametrize(
    ("from_status", "target_status"),
    [
        ("open", "resolved"),
        ("open", "closed"),
        ("in_progress", "open"),
        ("resolved", "in_progress"),
        ("closed", "open"),
        ("cancelled", "in_progress"),
        ("open", "open"),
    ],
)
def test_invalid_transitions_rejected(client, admin_headers, from_status, target_status):
    ticket = ticket_in_status(client, admin_headers, from_status)
    response = transition_status(client, admin_headers, ticket["id"], target_status)
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "invalid_status_transition"
    assert body["current_status"] == from_status
    assert body["requested_status"] == target_status

    detail = client.get(f"/api/tickets/{ticket['id']}", headers=admin_headers)
    assert detail.json()["status"] == from_status
