from pydantic import BaseModel


class InviteNotificationResponseSchema(BaseModel):
    project_name: str
    project_creator: str
    state: str
    date_time: str


class InviteNotificationsResponseSchemas(BaseModel):
    count: int
    invites: list[InviteNotificationResponseSchema]
