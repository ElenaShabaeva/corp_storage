from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from models.message_notification import MessageNotification
from uuid import UUID
from datetime import datetime


class MessageNotificationRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def post(
            self,
            message: str,
            message_datetime: datetime,
            from_user_id: UUID,
            to_user_id: UUID
    ) -> MessageNotification:
        message_notification = MessageNotification(
            message=message,
            message_datetime=message_datetime,
            is_read=False,
            from_user_id=from_user_id,
            to_user_id=to_user_id
        )

        self._db.add(message_notification)
        await self._db.flush()
        return message_notification
