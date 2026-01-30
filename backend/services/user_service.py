from sqlalchemy.ext.asyncio import AsyncSession
from repository.user_repository import UserRepository
from fastapi import Response, HTTPException, status
from schemas.request.user_request import RegistrationRequestSchema
from utils.hasher import hasher
from utils.jwt_utils import generate_token, decode_jwt
from utils.TokenTypeEnum import TokenType
from configuration import settings
from schemas.response.user_response import RegAuthResponseSchema
from schemas.internal.token_schema import TokenInfoSchema
from schemas.request.user_request import LoginRequestSchema
from jwt import ExpiredSignatureError


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repository: UserRepository = UserRepository(db=db)

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

        access_token = generate_token(user_id=user.id, token_type=TokenType.ACCESS)
        refresh_token = generate_token(user_id=user.id, token_type=TokenType.REFRESH)

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

        access_token = generate_token(user_id=user.id, token_type=TokenType.ACCESS)
        refresh_token = generate_token(user_id=user.id, token_type=TokenType.REFRESH)

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

    async def refresh_tokens(self, response: Response, refresh_token: str | None):
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token не найден"
            )
        try:
            user_id = decode_jwt(token=refresh_token)
            user = await self.user_repository.get_by_id(user_id=user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не найден"
                )

            access_token = generate_token(user_id=user.id, token_type=TokenType.ACCESS)
            refresh_token = generate_token(user_id=user.id, token_type=TokenType.REFRESH)

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

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен истек"
            )
