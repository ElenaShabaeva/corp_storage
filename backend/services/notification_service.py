from fastapi import HTTPException, status, Request
from utils.jwt_utils import decode_jwt
from typing import Dict
import asyncio
from uuid import UUID
import logging
from jwt import ExpiredSignatureError, DecodeError
from schemas.internal.notification_schema import (
    InviteNotificationSchema,
    MessageNotificationSchema
)


class NotificationService:
    def __init__(self):
        self.active_connections: Dict[UUID, asyncio.Queue] = {}
        self._lock = asyncio.Lock()
        self._logger = logging.getLogger()

    async def connect(self, access_token: str | None):
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            async with self._lock:
                if user_id not in self.active_connections:
                    self.active_connections[user_id] = asyncio.Queue()
                    self._logger.info(f"Пользователь {user_id} подключился. Всего подключений: {len(self.active_connections)}")
                return user_id
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

    async def disconnect(self, access_token: str | None):
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            async with self._lock:
                if user_id in self.active_connections:
                    del self.active_connections[user_id]
                    self._logger.info(f"Пользователь {user_id} отключен. Всего подключений: {len(self.active_connections)}")
                return True
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

    async def send_notification(
            self,
            user_id: UUID,
            notification: InviteNotificationSchema | MessageNotificationSchema
    ):
        async with self._lock:
            if user_id in self.active_connections:
                await self.active_connections[user_id].put(item=notification)
                self._logger.info(f"Уведомление отправлено {user_id}")

    async def event_generator(self, access_token: str | None, request: Request):
        user_id = await self.connect(access_token=access_token)
        queue = self.active_connections.get(user_id)
        if not queue:
            self._logger.info(f"Очередь пользователя {user_id} не найдена")
            return

        try:
            self._logger.info(f"Соединение для {user_id} установлено")

            while True:
                if await request.is_disconnected():
                    self._logger.info(f"Пользователь {user_id} отключился")
                    break
                try:
                    message = await asyncio.wait_for(queue.get(), timeout=1.0)
                    yield {
                        "event": "notification",
                        "data": message.model_dump_json()
                    }

                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    self._logger.info(f"Ошибка у user: {user_id}: {e}")
        finally:
            await self.disconnect(access_token=access_token)


notification_service = NotificationService()
