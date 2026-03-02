from pydantic import BaseModel
from uuid import UUID


class UserShortInfoSchema(BaseModel):
    id: UUID
    login: str
