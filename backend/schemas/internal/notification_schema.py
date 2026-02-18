from pydantic import BaseModel
from uuid import UUID


class InviteNotificationSchema(BaseModel):
    id: UUID
    project_name: str
    project_creator: str
    date_time: str
    state: str


class MessageNotificationSchema(BaseModel):
    id: UUID
    message: str
    date_time: str
