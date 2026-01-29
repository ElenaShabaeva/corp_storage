from pydantic import BaseModel


class RegistrationRequestSchema(BaseModel):
    login: str
    password: str
    name: str
    surname: str


class LoginRequestSchema(BaseModel):
    login: str
    password: str
