from pydantic import BaseModel
from uuid import UUID


class MessageNotificationResponseSchema(BaseModel):
    id: UUID
    message: str
    date_time: str
    is_read: bool


class MessagesNotificationResponseSchema(BaseModel):
    count: int
    messages: list[MessageNotificationResponseSchema]
