from fastapi import HTTPException, status
from utils.jwt_utils import decode_jwt
from jwt import ExpiredSignatureError, DecodeError
from utils.uow import UnitOfWork
from schemas.response.message_notification_response import (
    MessageNotificationResponseSchema,
    MessagesNotificationResponseSchema
)


class MessageNotificationService:
    def __init__(self):
        self.uow = UnitOfWork()

    async def get_all_message(self, access_token: str | None) -> MessagesNotificationResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)

            async with self.uow.start():
                messages = await self.uow.message_notifications.get_all(user_id=user_id)

            return MessagesNotificationResponseSchema(
                count=len(messages),
                messages=[MessageNotificationResponseSchema(
                    id=message.id,
                    message=message.message,
                    date_time=message.message_datetime.strftime("%d.%m.%Y / %H:%M"),
                    is_read=message.is_read
                ) for message in messages]
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
