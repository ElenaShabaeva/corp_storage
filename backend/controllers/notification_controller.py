from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from configuration import settings
from services.notification_service import NotificationService


router = APIRouter(
    prefix="/notification",
    tags=["Notification"]
)

notification_service = NotificationService()


@router.get("/connect")
async def connect(
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer)
):
    return await notification_service.connect(access_token=credentials.credentials)


@router.get("/disconnect")
async def disconnect(
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer)
):
    return await notification_service.disconnect(access_token=credentials.credentials)
