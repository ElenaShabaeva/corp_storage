from fastapi import APIRouter, Response, Depends
from services.user_service import UserService
from dependencies import get_user_service
from schemas.request.user_request import RegistrationRequestSchema, LoginRequestSchema
from schemas.response.user_response import RegistrationResponseSchema


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/registration", response_model=RegistrationResponseSchema)
async def registrate(
        payload: RegistrationRequestSchema,
        response: Response,
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.registrate(response=response, payload=payload)
