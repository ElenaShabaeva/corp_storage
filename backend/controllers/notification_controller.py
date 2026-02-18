from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
from configuration import settings
from services.notification_service import notification_service
from services.invite_notification_service import InviteNotificationService
from services.message_notification_service import MessageNotificationService
from services.project_service import ProjectService
from sse_starlette import EventSourceResponse
from schemas.response.invite_notification_response import InviteNotificationsResponseSchemas
from uuid import UUID
from schemas.response.standart_message import MessageResponseSchema
from schemas.response.message_notification_response import (
    MessagesNotificationResponseSchema,
    MessageNotificationResponseSchema
)

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


@router.post("/invites/accept", response_model=MessageResponseSchema)
async def accept_invite(
        invite_id: UUID,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        project_service: ProjectService = Depends(ProjectService)
):
    return await project_service.accept_invite(invite_id=invite_id, access_token=credentials.credentials)


@router.post("/invites/decline", response_model=MessageResponseSchema)
async def decline_invite(
        invite_id: UUID,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        project_service: ProjectService = Depends(ProjectService)
):
    return await project_service.decline_invite(invite_id=invite_id, access_token=credentials.credentials)


@router.delete("/invites/delete", response_model=MessageResponseSchema)
async def delete_invite(
        invite_id: UUID,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        invite_notification_service: InviteNotificationService = Depends(InviteNotificationService)
):
    return await invite_notification_service.delete_invite(invite_id=invite_id, access_token=credentials.credentials)


@router.delete("/invites/delete_all", response_model=MessageResponseSchema)
async def delete_all_invites(
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        invite_notification_service: InviteNotificationService = Depends(InviteNotificationService)
):
    return await invite_notification_service.delete_all_invites(access_token=credentials.credentials)


@router.get("/messages", response_model=MessagesNotificationResponseSchema)
async def get_all_messages(
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        message_notification_service: MessageNotificationService = Depends(MessageNotificationService)
):
    return await message_notification_service.get_all_message(access_token=credentials.credentials)


@router.patch("/messages/read", response_model=MessageNotificationResponseSchema)
async def read(
        message_id: UUID,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        messages_notification_service: MessageNotificationService = Depends(MessageNotificationService)
):
    return await messages_notification_service.read(message_id=message_id, access_token=credentials.credentials)


@router.patch("/messages/read-all", response_model=MessageResponseSchema)
async def read_all(
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        messages_notification_service: MessageNotificationService = Depends(MessageNotificationService)
):
    return await messages_notification_service.read_all(access_token=credentials.credentials)


@router.delete("/messages/delete", response_model=MessageResponseSchema)
async def delete_message(
        message_id: UUID,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        messages_notification_service: MessageNotificationService = Depends(MessageNotificationService)
):
    return await messages_notification_service.delete_message(message_id=message_id, access_token=credentials.credentials)
