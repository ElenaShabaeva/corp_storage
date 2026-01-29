import os
from configuration import settings
from datetime import datetime, timezone, timedelta
import jwt
import uuid
from jwt.exceptions import DecodeError
from uuid import UUID
from utils.TokenTypeEnum import TokenType


def encode_jwt(
        payload: dict,
        token_type: TokenType,
        private_key: str = os.getenv("PRIVATE_KEY"),
        algorithm: str = os.getenv("ALGORITHM")
):
    now = datetime.now(timezone.utc)
    if token_type == TokenType.ACCESS:
        expiration_minutes = settings.expiration_time_of_access_token
    elif token_type == TokenType.REFRESH:
        expiration_minutes = settings.expiration_time_of_refresh_token
    else:
        raise ValueError(f"Неизвестный тип токена")

    expiration_time = now + timedelta(minutes=expiration_minutes)
    payload.update({
        "exp": int(expiration_time.timestamp()),
        "iat": int(now.timestamp())
    })
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(
        token,
        public_key: str = os.getenv("PUBLIC_KEY"),
        algorithm: str = os.getenv("ALGORITHM")
):
    try:
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
            leeway=10
        )
        return uuid.UUID(decoded["sub"])
    except DecodeError as e:
        raise e


def generate_token(user_id: UUID, token_type: TokenType):
    payload = {"sub": str(user_id)}
    return encode_jwt(payload=payload, token_type=token_type)
