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
    is_read: bool
    date_time: str
