from fastapi.testclient import TestClient

STATUS_PATHS: dict[str, list[str]] = {
    "open": [],
    "in_progress": ["in_progress"],
    "resolved": ["in_progress", "resolved"],
    "closed": ["in_progress", "resolved", "closed"],
    "cancelled": ["cancelled"],
}


def create_ticket(
    client: TestClient,
    headers: dict[str, str],
    *,
    title: str = "Test ticket",
    description: str = "Test description",
    priority: str = "medium",
) -> dict:
    response = client.post(
        "/api/tickets",
        headers=headers,
        json={"title": title, "description": description, "priority": priority},
    )
    assert response.status_code == 201, response.text
    return response.json()


def transition_status(
    client: TestClient,
    headers: dict[str, str],
    ticket_id: int,
    status: str,
):
    return client.patch(
        f"/api/tickets/{ticket_id}/status",
        headers=headers,
        json={"status": status},
    )


def ticket_in_status(
    client: TestClient,
    headers: dict[str, str],
    status: str,
) -> dict:
    ticket = create_ticket(client, headers, title=f"Ticket for {status}")
    for step in STATUS_PATHS[status]:
        response = transition_status(client, headers, ticket["id"], step)
        assert response.status_code == 200, response.text
        ticket = response.json()
    return ticket
