from sqlalchemy.ext.asyncio import AsyncSession
from models.user_project_association import UserProjectAssociation
from uuid import UUID


class UserProjectAssociationRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def add_member(self, user_id: UUID, project_id: UUID):
        association = UserProjectAssociation(
            user_id=user_id,
            project_id=project_id
        )
        self.db.add(association)
