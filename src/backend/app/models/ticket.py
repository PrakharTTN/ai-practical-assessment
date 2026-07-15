from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import TicketPriority, TicketStatus


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[TicketPriority] = mapped_column(
        Enum(TicketPriority, name="ticket_priority", native_enum=True, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        index=True,
    )
    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus, name="ticket_status", native_enum=True, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=TicketStatus.OPEN,
        server_default=TicketStatus.OPEN.value,
        index=True,
    )
    assigned_to_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_by_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    assignee = relationship("User", back_populates="tickets_assigned", foreign_keys=[assigned_to_id])
    creator = relationship("User", back_populates="tickets_created", foreign_keys=[created_by_id])
    comments = relationship(
        "Comment",
        back_populates="ticket",
        cascade="all, delete-orphan",
        order_by="Comment.created_at",
    )
