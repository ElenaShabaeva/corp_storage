from fastapi import APIRouter, Response, Depends, Cookie
from services.user_service import UserService
from dependencies import get_user_service
from schemas.request.user_request import RegistrationRequestSchema, LoginRequestSchema
from schemas.response.user_response import RegAuthResponseSchema


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


@router.get("/refresh")
async def refresh_tokens(
        response: Response,
        refresh_token: str | None = Cookie(default=None),
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.refresh_tokens(response=response, refresh_token=refresh_token)
