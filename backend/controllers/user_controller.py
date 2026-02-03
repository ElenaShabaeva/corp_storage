from fastapi import APIRouter, Response, Depends, Cookie
from services.user_service import UserService
from dependencies import get_user_service
from fastapi.security import HTTPAuthorizationCredentials
from configuration import settings
from schemas.request.user_request import (
    RegistrationRequestSchema,
    LoginRequestSchema
)
from schemas.response.user_response import (
    UserInfoResponseSchema,
    LogoutResponseSchema,
    RegAuthResponseSchema
)


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/registration", response_model=RegAuthResponseSchema)
async def registrate(
        payload: RegistrationRequestSchema,
        response: Response,
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.registrate(response=response, payload=payload)


@router.post("/login", response_model=RegAuthResponseSchema)
async def login(
        payload: LoginRequestSchema,
        response: Response,
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.login(response=response, payload=payload)


@router.get("/logout", response_model=LogoutResponseSchema)
async def logout(
        response: Response,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.logout(response=response, encoded_jwt=credentials.credentials)


@router.get("/refresh", response_model=RegAuthResponseSchema)
async def refresh_tokens(
        response: Response,
        refresh_token: str | None = Cookie(default=None),
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.refresh_tokens(response=response, refresh_token=refresh_token)


@router.get("/profile", response_model=UserInfoResponseSchema)
async def get_profile(
        user_service: UserService = Depends(get_user_service),
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer)
):
    return await user_service.get_profile(encoded_jwt=credentials.credentials)
