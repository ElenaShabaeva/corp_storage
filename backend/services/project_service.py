from sqlalchemy.ext.asyncio import AsyncSession
from uow.project_uow import ProjectUnitOfWork
from fastapi import HTTPException, status
from utils.jwt_utils import decode_jwt
from jwt import ExpiredSignatureError, DecodeError
from schemas.request.project_request import (
    ProjectCreateRequestSchema
)
from schemas.response.project_response import (
    ProjectShortInfoResponseSchema,
    GetAllProjectsResponseSchema
)


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.project_uow: ProjectUnitOfWork = ProjectUnitOfWork(db=db)

    async def get_all(self, access_token: str | None) -> GetAllProjectsResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            projects = await self.project_uow.get_all(user_id=user_id)
            projects_response = [ProjectShortInfoResponseSchema(
                id=project.id,
                name=project.name,
                creator_login=project.creator.login,
                members_count=project.members_count
            ) for project in projects]
            return GetAllProjectsResponseSchema(
                count=len(projects_response),
                projects=projects_response
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

    async def create(
            self,
            payload: ProjectCreateRequestSchema,
            access_token: str | None
    ) -> ProjectShortInfoResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            new_project = await self.project_uow.create_project(
                name=payload.name,
                description=payload.description,
                creator_id=user_id
            )
            user = await self.user_repository.get_by_id(user_id=user_id)
            return ProjectShortInfoResponseSchema(
                id=new_project.id,
                name=new_project.name,
                creator_login=user.login,
                members_count=new_project.members_count
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
