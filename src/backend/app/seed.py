"""Seed sample users, tickets (all statuses), and comments. Idempotent."""

from passlib.context import CryptContext

from app.database import SessionLocal
from app.models import Comment, Ticket, TicketPriority, TicketStatus, User, UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dev-only — documented in database/seed-data/README.md (never shown in the UI)
DEFAULT_ADMIN_EMAIL = "admin@admin.com"
DEFAULT_ADMIN_PASSWORD = "admin"
DEFAULT_AGENT_EMAIL = "agent@example.com"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def seed() -> None:
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            print("[seed] Data already exists — skipping.")
            return

        admin = User(
            name="Admin User",
            email=DEFAULT_ADMIN_EMAIL,
            role=UserRole.ADMIN,
            password_hash=hash_password(DEFAULT_ADMIN_PASSWORD),
        )
        agent = User(
            name="Support Agent",
            email=DEFAULT_AGENT_EMAIL,
            role=UserRole.AGENT,
            password_hash=hash_password(DEFAULT_ADMIN_PASSWORD),
        )
        db.add_all([admin, agent])
        db.flush()

        tickets = [
            Ticket(
                title="Cannot reset password",
                description="User reports password reset email never arrives.",
                priority=TicketPriority.HIGH,
                status=TicketStatus.OPEN,
                created_by_id=admin.id,
                assigned_to_id=agent.id,
            ),
            Ticket(
                title="Dashboard loading slowly",
                description="Analytics dashboard takes 30+ seconds on first load.",
                priority=TicketPriority.MEDIUM,
                status=TicketStatus.IN_PROGRESS,
                created_by_id=agent.id,
                assigned_to_id=agent.id,
            ),
            Ticket(
                title="Export CSV missing columns",
                description="Exported file omits priority column.",
                priority=TicketPriority.LOW,
                status=TicketStatus.RESOLVED,
                created_by_id=admin.id,
                assigned_to_id=admin.id,
            ),
            Ticket(
                title="Typo in welcome email",
                description="Welcome email says 'Wellcome' instead of 'Welcome'.",
                priority=TicketPriority.LOW,
                status=TicketStatus.CLOSED,
                created_by_id=agent.id,
            ),
            Ticket(
                title="Duplicate charge on invoice",
                description="Customer billed twice for March subscription.",
                priority=TicketPriority.HIGH,
                status=TicketStatus.CANCELLED,
                created_by_id=admin.id,
            ),
            Ticket(
                title="Feature request: dark mode",
                description="Multiple users requested a dark theme option.",
                priority=TicketPriority.MEDIUM,
                status=TicketStatus.OPEN,
                created_by_id=agent.id,
            ),
        ]
        db.add_all(tickets)
        db.flush()

        comments = [
            Comment(
                ticket_id=tickets[0].id,
                message="Checked spam folder — no email found. Escalating to infra.",
                created_by_id=agent.id,
            ),
            Comment(
                ticket_id=tickets[1].id,
                message="Profiling shows N+1 query on dashboard widgets.",
                created_by_id=agent.id,
            ),
            Comment(
                ticket_id=tickets[2].id,
                message="Fix deployed; waiting for user confirmation.",
                created_by_id=admin.id,
            ),
            Comment(
                ticket_id=tickets[3].id,
                message="Template corrected and ticket closed.",
                created_by_id=agent.id,
            ),
        ]
        db.add_all(comments)
        db.commit()

        print(
            f"[seed] Created {db.query(User).count()} users, "
            f"{db.query(Ticket).count()} tickets, "
            f"{db.query(Comment).count()} comments."
        )
        print(
            f"[seed] Default admin account: {DEFAULT_ADMIN_EMAIL} "
            f"(password documented in database/seed-data/README.md)"
        )
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
