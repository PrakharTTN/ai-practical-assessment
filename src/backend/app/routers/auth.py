from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.exceptions import AppError
from app.models import User
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.user import UserOut
from app.services.auth import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Annotated[Session, Depends(get_db)]) -> LoginResponse:
    user = db.scalar(select(User).where(User.email == body.email))
    if user is None or not verify_password(body.password, user.password_hash):
        raise AppError(
            error="unauthorized",
            message="Invalid email or password",
            status_code=401,
        )

    token = create_access_token(user)
    return LoginResponse(access_token=token)


@router.get("/me", response_model=UserOut)
def get_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """Return the authenticated user's profile."""
    return current_user
