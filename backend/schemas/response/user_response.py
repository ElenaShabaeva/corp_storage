from pydantic import BaseModel
from uuid import UUID
from schemas.internal.token_schema import TokenInfoSchema


class RegistrationResponseSchema(BaseModel):
    id: UUID
    token_info: TokenInfoSchema
