from sqlalchemy.ext.asyncio import AsyncSession
from models.user_project_association import UserProjectAssociation
from uuid import UUID
from sqlalchemy import delete


class UserProjectAssociationRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def add_member(self, user_id: UUID, project_id: UUID) -> None:
        association = UserProjectAssociation(
            user_id=user_id,
            project_id=project_id
        )
        self.db.add(association)

    async def delete(self, user_id: UUID, project_id: UUID) -> int:
        result = await self.db.execute(
            delete(UserProjectAssociation)
            .where(UserProjectAssociation.project_id == project_id)
            .where(UserProjectAssociation.user_id == user_id)
        )

        return result.rowcount
