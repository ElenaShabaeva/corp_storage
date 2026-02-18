from fastapi import HTTPException, status
from utils.jwt_utils import decode_jwt
from jwt import ExpiredSignatureError, DecodeError
from utils.uow import UnitOfWork
from schemas.response.invite_notification_response import (
    InviteNotificationResponseSchema,
    InviteNotificationsResponseSchemas
)


class InviteNotificationService:
    def __init__(self):
        self.uow = UnitOfWork()

    async def get_all_invites(self, access_token: str | None) -> InviteNotificationsResponseSchemas:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            async with self.uow.start():
                invites = await self.uow.invite_notifications.get_by_user_id(to_user_id=user_id)

                return InviteNotificationsResponseSchemas(
                    count=len(invites),
                    invites=[InviteNotificationResponseSchema(
                        id=invite.id,
                        project_name=invite.project.name,
                        project_creator=invite.project.creator.login,
                        state=invite.state,
                        date_time=invite.invite_datetime.strftime("%d.%m.%Y / %H:%M"),
                    ) for invite in invites]
                )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token истек"
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный формат токена"
            )
