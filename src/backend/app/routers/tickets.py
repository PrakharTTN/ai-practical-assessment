import csv
import io
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.deps import get_current_user
from app.exceptions import AppError
from app.models import Comment, Ticket, TicketPriority, TicketStatus, User
from app.schemas.ticket import (
    CommentCreate,
    CommentOut,
    TicketCreate,
    TicketListOut,
    TicketOut,
    TicketStatusUpdate,
    TicketUpdate,
)
from app.services.ticket_state_machine import apply_status_transition

router = APIRouter(prefix="/tickets", tags=["tickets"])


def _get_user_or_404(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise AppError(
            error="not_found",
            message=f"User {user_id} not found",
            status_code=404,
        )
    return user


def _get_ticket_or_404(db: Session, ticket_id: int) -> Ticket:
    ticket = db.scalar(
        select(Ticket)
        .where(Ticket.id == ticket_id)
        .options(
            joinedload(Ticket.assignee),
            joinedload(Ticket.creator),
            joinedload(Ticket.comments).joinedload(Comment.author),
        )
    )
    if ticket is None:
        raise AppError(
            error="not_found",
            message=f"Ticket {ticket_id} not found",
            status_code=404,
        )
    return ticket


def _ticket_to_out(ticket: Ticket, include_comments: bool = True) -> TicketOut:
    return TicketOut.model_validate(ticket)


@router.get("", response_model=list[TicketListOut])
def list_tickets(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
    status: TicketStatus | None = None,
    priority: TicketPriority | None = None,
    search: str | None = Query(default=None, max_length=200),
) -> list[TicketListOut]:
    stmt = select(Ticket).options(
        joinedload(Ticket.assignee),
        joinedload(Ticket.creator),
    )
    if status is not None:
        stmt = stmt.where(Ticket.status == status)
    if priority is not None:
        stmt = stmt.where(Ticket.priority == priority)
    if search:
        stmt = stmt.where(Ticket.title.ilike(f"%{search}%"))
    stmt = stmt.order_by(Ticket.created_at.desc())
    tickets = list(db.scalars(stmt).unique().all())
    return [TicketListOut.model_validate(t) for t in tickets]


@router.post("", response_model=TicketOut, status_code=201)
def create_ticket(
    body: TicketCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> TicketOut:
    if body.assigned_to_id is not None:
        _get_user_or_404(db, body.assigned_to_id)

    ticket = Ticket(
        title=body.title,
        description=body.description,
        priority=body.priority,
        status=TicketStatus.OPEN,
        assigned_to_id=body.assigned_to_id,
        created_by_id=current_user.id,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    ticket = _get_ticket_or_404(db, ticket.id)
    return _ticket_to_out(ticket, include_comments=True)


@router.get("/export")
def export_tickets_csv(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Response:
    tickets = db.scalars(
        select(Ticket)
        .where(Ticket.created_by_id == current_user.id)
        .options(joinedload(Ticket.assignee))
        .order_by(Ticket.created_at.desc())
    ).unique().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "id",
            "title",
            "description",
            "priority",
            "status",
            "assigned_to_email",
            "created_at",
            "updated_at",
        ]
    )
    for ticket in tickets:
        writer.writerow(
            [
                ticket.id,
                ticket.title,
                ticket.description,
                ticket.priority.value,
                ticket.status.value,
                ticket.assignee.email if ticket.assignee else "",
                ticket.created_at.isoformat(),
                ticket.updated_at.isoformat(),
            ]
        )

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=tickets_export.csv"},
    )


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(
    ticket_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
) -> TicketOut:
    ticket = _get_ticket_or_404(db, ticket_id)
    return _ticket_to_out(ticket)


@router.patch("/{ticket_id}", response_model=TicketOut)
def update_ticket(
    ticket_id: int,
    body: TicketUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
) -> TicketOut:
    ticket = _get_ticket_or_404(db, ticket_id)
    updates = body.model_dump(exclude_unset=True)

    if not updates:
        raise AppError(
            error="validation_error",
            message="No fields provided to update",
            status_code=422,
        )

    if "assigned_to_id" in updates and updates["assigned_to_id"] is not None:
        _get_user_or_404(db, updates["assigned_to_id"])

    for field, value in updates.items():
        setattr(ticket, field, value)
    ticket.updated_at = datetime.now(timezone.utc)

    db.commit()
    ticket = _get_ticket_or_404(db, ticket_id)
    return _ticket_to_out(ticket)


@router.patch("/{ticket_id}/status", response_model=TicketOut)
def update_ticket_status(
    ticket_id: int,
    body: TicketStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
) -> TicketOut:
    ticket = _get_ticket_or_404(db, ticket_id)
    apply_status_transition(ticket, body.status)
    ticket.updated_at = datetime.now(timezone.utc)
    db.commit()
    ticket = _get_ticket_or_404(db, ticket_id)
    return _ticket_to_out(ticket)


@router.post("/{ticket_id}/comments", response_model=CommentOut, status_code=201)
def add_comment(
    ticket_id: int,
    body: CommentCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> CommentOut:
    _get_ticket_or_404(db, ticket_id)
    comment = Comment(
        ticket_id=ticket_id,
        message=body.message,
        created_by_id=current_user.id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    comment = db.scalar(
        select(Comment)
        .where(Comment.id == comment.id)
        .options(joinedload(Comment.author))
    )
    return CommentOut.model_validate(comment)
