from pydantic import BaseModel, Field, field_validator
import re


class RegistrationRequestSchema(BaseModel):
    login: str = Field(min_length=4, max_length=16)
    password: str = Field(min_length=8, max_length=16)
    name: str = Field(min_length=1, max_length=150)
    surname: str = Field(min_length=1, max_length=150)

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"[a-z]", value):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not re.search(r"\d", value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        return value


class LoginRequestSchema(BaseModel):
    login: str = Field(min_length=4, max_length=16)
    password: str = Field(min_length=8, max_length=16)
