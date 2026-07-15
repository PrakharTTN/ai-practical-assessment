from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_admin
from app.exceptions import AppError
from app.models import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.auth import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserOut])
def list_users(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
) -> list[User]:
    """Return users for assignee picker (no password data)."""
    return list(db.scalars(select(User).order_by(User.name)).all())


@router.post("", response_model=UserOut, status_code=201)
def create_user(
    body: UserCreate,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)],
) -> User:
    """Create a new user (admin only)."""
    existing = db.scalar(select(User).where(User.email == body.email))
    if existing is not None:
        raise AppError(
            error="duplicate_email",
            message="A user with this email already exists",
            status_code=409,
            details={"email": ["Email already registered"]},
        )

    user = User(
        name=body.name.strip(),
        email=body.email.lower(),
        role=body.role,
        password_hash=hash_password(body.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    body: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_admin)],
) -> User:
    """Update an existing user (admin only)."""
    if not any(
        value is not None
        for value in (body.name, body.email, body.password, body.role)
    ):
        raise AppError(
            error="validation_error",
            message="At least one field must be provided",
            status_code=422,
        )

    user = db.get(User, user_id)
    if user is None:
        raise AppError(
            error="not_found",
            message="User not found",
            status_code=404,
        )

    if body.email is not None:
        normalized = body.email.lower()
        existing = db.scalar(
            select(User).where(User.email == normalized, User.id != user_id)
        )
        if existing is not None:
            raise AppError(
                error="duplicate_email",
                message="A user with this email already exists",
                status_code=409,
                details={"email": ["Email already registered"]},
            )
        user.email = normalized

    if body.name is not None:
        user.name = body.name.strip()

    if body.role is not None:
        user.role = body.role

    if body.password is not None:
        user.password_hash = hash_password(body.password)

    db.commit()
    db.refresh(user)
    return user
