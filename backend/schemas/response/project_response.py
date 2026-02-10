from pydantic import BaseModel


class ProjectShortInfoResponseSchema(BaseModel):
    name: str
    creator_login: str
    members_count: int

    class Config:
        from_attributes = True


class GetAllProjectsResponseSchema(BaseModel):
    count: int
    projects: list[ProjectShortInfoResponseSchema]
