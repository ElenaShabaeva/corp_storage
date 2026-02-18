from pydantic import BaseModel


class InviteNotificationSchema(BaseModel):
    project_name: str
    project_creator: str
    date_time: str


class MessageNotificationSchema(BaseModel):
    message: str
    date_time: str
