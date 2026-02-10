from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from schemas.internal.user_schema import UserShortInfoSchema


class ProjectShortInfoResponseSchema(BaseModel):
    id: UUID
    name: str
    creator_login: str
    members_count: int


class ProjectFullInfoResponseSchema(ProjectShortInfoResponseSchema):
    isOwner: bool
    description: Optional[str] = None
    members: list[UserShortInfoSchema]


class GetAllProjectsResponseSchema(BaseModel):
    count: int
    projects: list[ProjectShortInfoResponseSchema]
