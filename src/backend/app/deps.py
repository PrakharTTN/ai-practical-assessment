from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import AppError
from app.models import User
from app.models.enums import UserRole
from app.services.auth import decode_access_token

security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AppError(
            error="unauthorized",
            message="Authentication required",
            status_code=401,
        )

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise AppError(
            error="unauthorized",
            message="Invalid or expired token",
            status_code=401,
        ) from None

    user = db.get(User, user_id)
    if user is None:
        raise AppError(
            error="unauthorized",
            message="Invalid or expired token",
            status_code=401,
        )
    return user


def require_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise AppError(
            error="forbidden",
            message="Admin access required",
            status_code=403,
        )
    return current_user
