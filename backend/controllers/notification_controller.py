from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
from configuration import settings
from services.notification_service import notification_service
from sse_starlette import EventSourceResponse


router = APIRouter(
    prefix="/notification",
    tags=["Notification"]
)


@router.get("/connect")
async def connect(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
):
    return EventSourceResponse(
        notification_service.event_generator(access_token=credentials.credentials, request=request)
    )


@router.get("/disconnect")
async def disconnect(
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer)
):
    return await notification_service.disconnect(access_token=credentials.credentials)
