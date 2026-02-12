from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from schemas.internal.user_schema import UserShortInfoSchema


class ProjectShortInfoResponseSchema(BaseModel):
    id: UUID
    name: str
    creator_login: str
    members_count: int


class ProjectMainPageInfoResponseSchema(BaseModel):
    id: UUID
    name: str
    description: str
    isOwner: bool


class ProjectMembersResponseSchema(BaseModel):
    members_count: int
    members: list[UserShortInfoSchema]


class GetAllProjectsResponseSchema(BaseModel):
    count: int
    projects: list[ProjectShortInfoResponseSchema]
