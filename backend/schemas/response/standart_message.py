from pydantic import BaseModel


class MessageResponseSchema(BaseModel):
    status: str
    message: str
