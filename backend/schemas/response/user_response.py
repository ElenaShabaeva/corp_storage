from pydantic import BaseModel
from uuid import UUID
from schemas.internal.token_schema import TokenInfoSchema


class RegAuthResponseSchema(BaseModel):
    id: UUID
    token_info: TokenInfoSchema


class UserInfoResponseSchema(BaseModel):
    id: UUID
    name: str
    surname: str
    login: str


class LogoutResponseSchema(BaseModel):
    status: str
    message: str


class UserDeleteResponseSchema(BaseModel):
    status: str
    rowcount: int
