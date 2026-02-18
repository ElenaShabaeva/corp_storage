from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from models.invite_notification import InviteNotification
from models.project import Project
from uuid import UUID
from datetime import datetime
from schemas.internal.invite_status_enum import InviteStatus


class InviteNotificationRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def post(
            self,
            project_id: UUID,
            invite_datetime: datetime,
            from_user_id: UUID,
            to_user_id: UUID
    ) -> InviteNotification:
        invite_notification = InviteNotification(
            state=InviteStatus.SENT,
            project_id=project_id,
            invite_datetime=invite_datetime,
            from_user_id=from_user_id,
            to_user_id=to_user_id
        )

        self._db.add(invite_notification)
        await self._db.flush()
        return invite_notification

    async def get_by_user_and_project_ids(self, to_user_id: UUID, project_id: UUID) -> InviteNotification | None:
        result = await self._db.execute(
            select(InviteNotification)
            .where(InviteNotification.to_user_id == to_user_id)
            .where(InviteNotification.project_id == project_id)
        )

        invite_notification = result.scalar_one_or_none()
        return invite_notification

    async def get_by_user_id(self, to_user_id: UUID) -> Sequence[InviteNotification]:
        result = await self._db.execute(
            select(InviteNotification)
            .where(InviteNotification.to_user_id == to_user_id)
            .options(
                selectinload(InviteNotification.project)
                .selectinload(Project.creator)
            )
        )
        invites = result.scalars().all()
        return invites
