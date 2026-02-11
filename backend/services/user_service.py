from utils.hasher import hasher
from utils.jwt_utils import generate_token, decode_jwt
from utils.TokenTypeEnum import TokenType
from configuration import settings
from schemas.internal.token_schema import TokenInfoSchema
from jwt import ExpiredSignatureError
from schemas.response.user_response import UserInfoResponseSchema
from jwt import DecodeError
from utils.uow import UnitOfWork
from fastapi import (
    Response,
    HTTPException,
    status,
    Request
)
from schemas.request.user_request import (
    RegistrationRequestSchema,
    LoginRequestSchema,
    UserPatchRequestSchema
)
from schemas.response.user_response import (
    RegAuthResponseSchema,
    LogoutResponseSchema,
    UserDeleteResponseSchema
)


class UserService:
    def __init__(self):
        self.uow = UnitOfWork()

    async def registrate(self, response: Response, payload: RegistrationRequestSchema) -> RegAuthResponseSchema:
        async with self.uow.start():
            optional_user = await self.uow.users.get_by_login(login=payload.login)

            if optional_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Пользователь с таким login уже существует"
                )

            user = await self.uow.users.post(
                name=payload.name,
                surname=payload.surname,
                login=payload.login,
                password=hasher.get_hash(item=payload.password)
            )

            access_token, _, _ = generate_token(user_id=user.id, token_type=TokenType.ACCESS)
            refresh_token, expires_at, jti = generate_token(user_id=user.id, token_type=TokenType.REFRESH)

            await self.uow.refresh_tokens.post(
                token_hash=hasher.get_hash(item=refresh_token),
                jti=jti,
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
        async with self.uow.start():
            user = await self.uow.users.get_by_login(login=payload.login)
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

            access_token, _, _ = generate_token(user_id=user.id, token_type=TokenType.ACCESS)
            refresh_token, expires_at, jti = generate_token(user_id=user.id, token_type=TokenType.REFRESH)

            await self.uow.refresh_tokens.post(
                token_hash=hasher.get_hash(item=refresh_token),
                jti=jti,
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

    async def logout(self, response: Response, request: Request) -> LogoutResponseSchema:
        try:
            refresh_token = request.cookies.get("refresh_token")
            if not refresh_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh токен не найден"
                )
            _, jti = decode_jwt(token=refresh_token)
            async with self.uow.start():
                refresh_token = await self.uow.refresh_tokens.get_by_jti(jti=jti)
                await self.uow.refresh_tokens.set_revoked_at(refresh_token=refresh_token)

            response.delete_cookie(key="refresh_token", secure=True, samesite='none', httponly=True)

            return LogoutResponseSchema(
                status="success",
                message="Выход был успешно завершен"
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен истек"
            )

    async def refresh_tokens(self, response: Response, refresh_token: str | None) -> RegAuthResponseSchema:
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token не найден"
            )
        try:
            user_id, jti = decode_jwt(token=refresh_token)
            async with self.uow.start():
                old_refresh_token = await self.uow.refresh_tokens.get_by_jti(
                    jti=jti
                )
                if not old_refresh_token:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Токен не найден в базе данных"
                    )
                await self.uow.refresh_tokens.set_revoked_at(refresh_token=old_refresh_token)

                access_token, _, _ = generate_token(user_id=user_id, token_type=TokenType.ACCESS)
                refresh_token, expires_at, jti = generate_token(user_id=user_id, token_type=TokenType.REFRESH)

                await self.uow.refresh_tokens.post(
                    token_hash=hasher.get_hash(item=refresh_token),
                    jti=jti,
                    user_id=user_id,
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
                id=user_id,
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

    async def get_profile(self, encoded_jwt: str | None) -> UserInfoResponseSchema:
        if not encoded_jwt:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен не найден"
            )
        try:
            user_id, _ = decode_jwt(token=encoded_jwt)
            async with self.uow.start():
                user = await self.uow.users.get_by_id(user_id=user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не найден"
                )
            return UserInfoResponseSchema(
                id=user.id,
                name=user.name,
                surname=user.surname,
                login=user.login
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен истек"
            )

    async def update_profile(self, payload: UserPatchRequestSchema, encoded_jwt: str | None) -> UserInfoResponseSchema:
        if not encoded_jwt:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен не найден"
            )
        try:
            user_id, _ = decode_jwt(token=encoded_jwt)
            async with self.uow.start():
                user = await self.uow.users.get_by_id(user_id=user_id)
                if payload.name:
                    user.name = payload.name
                if payload.surname:
                    user.surname = payload.surname
                updated_user = await self.uow.users.patch(updated_user=user)

            return UserInfoResponseSchema(
                id=updated_user.id,
                name=updated_user.name,
                surname=updated_user.surname,
                login=updated_user.login
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен истек"
            )

    async def delete_profile(
            self,
            encoded_jwt: str | None,
            response: Response,
            refresh_token: str | None
    ) -> UserDeleteResponseSchema:
        if not encoded_jwt:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен не найден"
            )
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token не найден"
            )
        try:
            _, jti = decode_jwt(token=refresh_token)
            async with self.uow.start():
                refresh_token = await self.uow.refresh_tokens.get_by_jti(jti=jti)
                await self.uow.refresh_tokens.set_revoked_at(refresh_token=refresh_token)
                user_id, _ = decode_jwt(token=encoded_jwt)
                rowcount = await self.uow.users.delete(user_id=user_id)
            response.delete_cookie(
                key="refresh_token",
                httponly=True,
                secure=True,
                samesite="none",
            )
            return UserDeleteResponseSchema(
                status="success",
                rowcount=rowcount
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен истек"
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неправильный формат токена"
            )
