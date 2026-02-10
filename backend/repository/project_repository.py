from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.project import Project
from models.user import User
from models.user_project_association import UserProjectAssociation
from uuid import UUID


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_all(self, user_id: UUID) -> Sequence[Project] | None:
        result = await self.db.execute(
            select(Project)
            .join(UserProjectAssociation, UserProjectAssociation.project_id == Project.id)
            .where(UserProjectAssociation.user_id == user_id)
            .options(selectinload(Project.creator))
        )

        projects = result.scalars().all()
        return projects

    async def post(
            self,
            name: str,
            creator_id: UUID,
            description: str | None = None,
    ) -> Project:
        project = Project(
            name=name,
            description=description,
            members_count=0,
            creator_id=creator_id
        )
        self.db.add(project)
        await self.db.flush()
        return project
