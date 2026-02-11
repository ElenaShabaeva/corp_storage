from contextlib import asynccontextmanager
from repository.user_repository import UserRepository
from repository.project_repository import ProjectRepository
from repository.user_project_association_repository import UserProjectAssociationRepository
from repository.refresh_token_repository import RefreshTokenRepository
from database.database import async_session


class UnitOfWork:
    def __init__(self):
        self._session_factory = async_session
        self._session = None

    @asynccontextmanager
    async def start(self):
        async with self._session_factory() as session:
            self._session = session
            try:
                yield self
                await self._session.commit()
            except Exception as e:
                await self._session.rollback()
                raise e
            finally:
                self._session = None

    @property
    def users(self) -> UserRepository:
        return UserRepository(db=self._session)

    @property
    def projects(self) -> ProjectRepository:
        return ProjectRepository(db=self._session)

    @property
    def user_project_association(self) -> UserProjectAssociationRepository:
        return UserProjectAssociationRepository(db=self._session)

    @property
    def refresh_tokens(self) -> RefreshTokenRepository:
        return RefreshTokenRepository(db=self._session)
