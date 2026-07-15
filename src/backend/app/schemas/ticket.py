from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import TicketPriority, TicketStatus
from app.schemas.user import UserOut


class TicketCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=5000)
    priority: TicketPriority
    assigned_to_id: int | None = None


class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=5000)
    priority: TicketPriority | None = None
    assigned_to_id: int | None = None


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class CommentCreate(BaseModel):
    message: str = Field(min_length=1, max_length=5000)


class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    message: str
    created_by: UserOut = Field(validation_alias="author")
    created_at: datetime


class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    title: str
    description: str
    priority: TicketPriority
    status: TicketStatus
    assigned_to: UserOut | None = Field(default=None, validation_alias="assignee")
    created_by: UserOut = Field(validation_alias="creator")
    created_at: datetime
    updated_at: datetime
    comments: list[CommentOut] = []


class TicketListOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    title: str
    description: str
    priority: TicketPriority
    status: TicketStatus
    assigned_to: UserOut | None = Field(default=None, validation_alias="assignee")
    created_by: UserOut = Field(validation_alias="creator")
    created_at: datetime
    updated_at: datetime
