from sqlalchemy.ext.asyncio import AsyncSession
from repository.user_repository import UserRepository
from repository.refresh_token_repository import RefreshTokenRepository
from fastapi import Response, HTTPException, status
from utils.hasher import hasher
from utils.jwt_utils import generate_token, decode_jwt
from utils.TokenTypeEnum import TokenType
from configuration import settings
from schemas.internal.token_schema import TokenInfoSchema
from schemas.request.user_request import (
    RegistrationRequestSchema,
    LoginRequestSchema
)
from schemas.response.user_response import (
    RegAuthResponseSchema
)


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repository: UserRepository = UserRepository(db=db)
        self.refresh_token_repository: RefreshTokenRepository = RefreshTokenRepository(db=db)

    async def registrate(self, response: Response, payload: RegistrationRequestSchema) -> RegAuthResponseSchema:
        optional_user = await self.user_repository.get_by_login(login=payload.login)
        if optional_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким login уже существует"
            )

        user = await self.user_repository.post(
            name=payload.name,
            surname=payload.surname,
            login=payload.login,
            password=hasher.get_hash(item=payload.password)
        )

        access_token, _ = generate_token(user_id=user.id, token_type=TokenType.ACCESS)
        refresh_token, expires_at = generate_token(user_id=user.id, token_type=TokenType.REFRESH)

        await self.refresh_token_repository.post(
            token_hash=hasher.get_hash(item=refresh_token),
            user_id=user.id,
            expires_at=expires_at
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=settings.expiration_time_of_refresh_token_for_browser
        )

        return RegAuthResponseSchema(
            id=user.id,
            token_info=TokenInfoSchema(
                token=access_token,
                token_type="Bearer"
            )
        )

    async def login(self, response: Response, payload: LoginRequestSchema) -> RegAuthResponseSchema:
        user = await self.user_repository.get_by_login(login=payload.login)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Неправильно введен логин или пароль"
            )
        if not hasher.match_hash(item=payload.password, item_hash=user.password):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Неправильно введен логин или пароль"
            )

        access_token, _ = generate_token(user_id=user.id, token_type=TokenType.ACCESS)
        refresh_token, expires_at = generate_token(user_id=user.id, token_type=TokenType.REFRESH)

        await self.refresh_token_repository.post(
            token_hash=hasher.get_hash(item=refresh_token),
            user_id=user.id,
            expires_at=expires_at
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=settings.expiration_time_of_refresh_token_for_browser
        )

        return RegAuthResponseSchema(
            id=user.id,
            token_info=TokenInfoSchema(
                token=access_token,
                token_type="Bearer"
            )
        )
