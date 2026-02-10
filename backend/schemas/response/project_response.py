from pydantic import BaseModel
from uuid import UUID


class ProjectShortInfoResponseSchema(BaseModel):
    id: UUID
    name: str
    creator_login: str
    members_count: int

    class Config:
        from_attributes = True


class GetAllProjectsResponseSchema(BaseModel):
    count: int
    projects: list[ProjectShortInfoResponseSchema]
