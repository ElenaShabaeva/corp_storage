from pydantic import BaseModel
from uuid import UUID


class InviteNotificationResponseSchema(BaseModel):
    id: UUID
    project_name: str
    project_creator: str
    state: str
    date_time: str


class InviteNotificationsResponseSchemas(BaseModel):
    count: int
    invites: list[InviteNotificationResponseSchema]
