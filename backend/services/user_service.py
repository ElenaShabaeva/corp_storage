from sqlalchemy.ext.asyncio import AsyncSession
from repository.user_repository import UserRepository
from fastapi import Response, HTTPException, status
from schemas.request.user_request import RegistrationRequestSchema
from utils.hasher import hasher
from utils.jwt_utils import generate_token, decode_jwt
from utils.TokenTypeEnum import TokenType
from configuration import settings
from schemas.response.user_response import RegistrationResponseSchema
from schemas.internal.token_schema import TokenInfoSchema
from schemas.request.user_request import LoginRequestSchema


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repository: UserRepository = UserRepository(db=db)

    async def registrate(self, response: Response, payload: RegistrationRequestSchema) -> RegistrationResponseSchema:
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

        return RegistrationResponseSchema(
            id=user.id,
            token_info=TokenInfoSchema(
                token=access_token,
                token_type="Bearer"
            )
        )
