"""Initial schema: users, tickets, comments

Revision ID: 001
Revises:
Create Date: 2026-07-10
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

user_role = postgresql.ENUM("agent", "admin", name="user_role", create_type=False)
ticket_priority = postgresql.ENUM("low", "medium", "high", name="ticket_priority", create_type=False)
ticket_status = postgresql.ENUM(
    "open", "in_progress", "resolved", "closed", "cancelled", name="ticket_status", create_type=False
)


def upgrade() -> None:
    user_role.create(op.get_bind(), checkfirst=True)
    ticket_priority.create(op.get_bind(), checkfirst=True)
    ticket_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "tickets",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("priority", ticket_priority, nullable=False),
        sa.Column("status", ticket_status, server_default="open", nullable=False),
        sa.Column("assigned_to_id", sa.Integer(), nullable=True),
        sa.Column("created_by_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["assigned_to_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tickets_priority", "tickets", ["priority"])
    op.create_index("ix_tickets_status", "tickets", ["status"])
    op.create_index("ix_tickets_assigned_to_id", "tickets", ["assigned_to_id"])
    op.create_index("ix_tickets_created_by_id", "tickets", ["created_by_id"])

    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("ticket_id", sa.Integer(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_comments_ticket_id", "comments", ["ticket_id"])


def downgrade() -> None:
    op.drop_index("ix_comments_ticket_id", table_name="comments")
    op.drop_table("comments")
    op.drop_index("ix_tickets_created_by_id", table_name="tickets")
    op.drop_index("ix_tickets_assigned_to_id", table_name="tickets")
    op.drop_index("ix_tickets_status", table_name="tickets")
    op.drop_index("ix_tickets_priority", table_name="tickets")
    op.drop_table("tickets")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    ticket_status.drop(op.get_bind(), checkfirst=True)
    ticket_priority.drop(op.get_bind(), checkfirst=True)
    user_role.drop(op.get_bind(), checkfirst=True)
