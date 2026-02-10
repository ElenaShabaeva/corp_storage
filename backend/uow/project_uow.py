from sqlalchemy.ext.asyncio import AsyncSession
from repository.project_repository import ProjectRepository
from repository.user_project_association_repository import UserProjectAssociationRepository
from uuid import UUID


class ProjectUnitOfWork:
    def __init__(self, db: AsyncSession):
        self._db: AsyncSession = db
        self._project_repository: ProjectRepository = ProjectRepository(db=db)
        self._association_repository: UserProjectAssociationRepository = UserProjectAssociationRepository(db=db)

    async def create_project(
            self,
            name: str,
            description: str | None,
            creator_id: UUID
    ):
        async with self._db.begin():
            project = await self._project_repository.post(
                name=name,
                description=description,
                creator_id=creator_id
            )
            await self._association_repository.add_member(user_id=creator_id, project_id=project.id)
            project.members_count += 1
        return project

    async def get_all(self, user_id: UUID):
        return await self._project_repository.get_all(user_id=user_id)
