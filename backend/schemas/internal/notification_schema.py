from pydantic import BaseModel
from datetime import datetime


class InviteNotificationSchema(BaseModel):
    project_name: str
    project_creator: str
    date_time: datetime


class MessageNotificationSchema(BaseModel):
    message: str
    date_time: datetime
