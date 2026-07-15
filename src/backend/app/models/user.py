from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role", native_enum=True, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    tickets_created = relationship(
        "Ticket",
        back_populates="creator",
        foreign_keys="Ticket.created_by_id",
    )
    tickets_assigned = relationship(
        "Ticket",
        back_populates="assignee",
        foreign_keys="Ticket.assigned_to_id",
    )
    comments = relationship("Comment", back_populates="author")
