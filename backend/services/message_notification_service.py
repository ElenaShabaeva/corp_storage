from fastapi import HTTPException, status
from utils.jwt_utils import decode_jwt
from jwt import ExpiredSignatureError, DecodeError
from utils.uow import UnitOfWork
from uuid import UUID
from schemas.response.standart_message import MessageResponseSchema
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

    async def read(self, message_id: UUID, access_token: str | None) -> MessageNotificationResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)

            async with self.uow.start():
                message = await self.uow.message_notifications.get_by_id(
                    message_id=message_id,
                    user_id=user_id
                )
                if not message:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Сообщение не найдено"
                    )
                message.is_read = True

            return MessageNotificationResponseSchema(
                id=message.id,
                message=message.message,
                date_time=message.message_datetime.strftime("%d.%m.%Y / %H:%M"),
                is_read=message.is_read
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

    async def read_all(self, access_token: str | None) -> MessageResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)

            async with self.uow.start():
                messages = await self.uow.message_notifications.get_all_unread(user_id=user_id)
                for message in messages:
                    message.is_read = True

            return MessageResponseSchema(
                status="success",
                message=f"Прочитано сообщений: {len(messages)}"
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

    async def delete_message(self, message_id: UUID, access_token: str | None) -> MessageResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)

            async with self.uow.start():
                rowcount = await self.uow.message_notifications.delete(
                    message_id=message_id,
                    user_id=user_id
                )

            return MessageResponseSchema(
                status="success",
                message=f"Удалено записей: {rowcount}"
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

    async def delete_all(self, access_token: str | None) -> MessageResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)

            async with self.uow.start():
                rowcount = await self.uow.message_notifications.delete_all(user_id=user_id)

            return MessageResponseSchema(
                status="success",
                message=f"Удалено записей: {rowcount}"
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
