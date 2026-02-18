from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
from configuration import settings
from services.notification_service import notification_service
from services.invite_notification_service import InviteNotificationService
from services.project_service import ProjectService
from sse_starlette import EventSourceResponse
from schemas.response.invite_notification_response import InviteNotificationsResponseSchemas
from uuid import UUID


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


@router.get("/invites", response_model=InviteNotificationsResponseSchemas)
async def get_all_invites(
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        invite_notification_service: InviteNotificationService = Depends(InviteNotificationService)
):
    return await invite_notification_service.get_all_invites(access_token=credentials.credentials)


@router.post("/invites/accept/{invite_id}")
async def accept_invite(
        invite_id: UUID,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        project_service: ProjectService = Depends(ProjectService)
):
    return await project_service.accept_invite(invite_id=invite_id, access_token=credentials.credentials)
