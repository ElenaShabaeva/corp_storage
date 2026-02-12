from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from utils.jwt_utils import decode_jwt
from jwt import ExpiredSignatureError, DecodeError
from utils.uow import UnitOfWork
from uuid import UUID
from schemas.request.project_request import (
    ProjectCreateRequestSchema
)
from schemas.internal.user_schema import (
    UserShortInfoSchema
)
from schemas.response.project_response import (
    ProjectShortInfoResponseSchema,
    GetAllProjectsResponseSchema,
    ProjectMainPageInfoResponseSchema,
    ProjectMembersResponseSchema
)


class ProjectService:
    def __init__(self):
        self.uow = UnitOfWork()

    async def get_all(self, access_token: str | None) -> GetAllProjectsResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            async with self.uow.start():
                projects = await self.uow.projects.get_all(user_id=user_id)
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
            async with self.uow.start():
                new_project = await self.uow.projects.post(
                    name=payload.name,
                    description=payload.description,
                    creator_id=user_id
                )
                await self.uow.user_project_association.add_member(
                    user_id=user_id,
                    project_id=new_project.id
                )
                new_project.members_count += 1
                user = await self.uow.users.get_by_id(user_id=user_id)
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

    async def get_by_id(self, project_id: UUID, access_token: str | None):
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            async with self.uow.start():
                project = await self.uow.projects.get_by_id(project_id=project_id)
                if not project:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Проект не найден"
                    )

                return ProjectMainPageInfoResponseSchema(
                    id=project.id,
                    name=project.name,
                    description=project.description,
                    isOwner=True if project.creator_id == user_id else False
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

    async def get_members(self, project_id: UUID, access_token: str | None):
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            async with self.uow.start():
                project = await self.uow.projects.get_by_id(project_id=project_id)
                members = await self.uow.projects.get_members(project_id=project_id)

            return ProjectMembersResponseSchema(
                members_count=project.members_count,
                members=[UserShortInfoSchema(
                    id=member.id,
                    login=member.login
                ) for member in members]
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
