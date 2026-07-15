from app.exceptions import AppError
from app.models import Ticket, TicketStatus


ALLOWED_TRANSITIONS: dict[TicketStatus, set[TicketStatus]] = {
    TicketStatus.OPEN: {TicketStatus.IN_PROGRESS, TicketStatus.CANCELLED},
    TicketStatus.IN_PROGRESS: {TicketStatus.RESOLVED, TicketStatus.CANCELLED},
    TicketStatus.RESOLVED: {TicketStatus.CLOSED},
    TicketStatus.CLOSED: set(),
    TicketStatus.CANCELLED: set(),
}


class InvalidStatusTransitionError(AppError):
    def __init__(self, current_status: str, requested_status: str) -> None:
        super().__init__(
            error="invalid_status_transition",
            message=f"Cannot transition from '{current_status}' to '{requested_status}'",
            status_code=400,
            current_status=current_status,
            requested_status=requested_status,
        )


def validate_transition(current: TicketStatus, target: TicketStatus) -> None:
    if current == target:
        raise InvalidStatusTransitionError(current.value, target.value)
    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if target not in allowed:
        raise InvalidStatusTransitionError(current.value, target.value)


def apply_status_transition(ticket: Ticket, target: TicketStatus) -> Ticket:
    validate_transition(ticket.status, target)
    ticket.status = target
    return ticket
