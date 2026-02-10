from sqlalchemy.ext.asyncio import AsyncSession
from repository.project_repository import ProjectRepository
from fastapi import HTTPException, status
from utils.jwt_utils import decode_jwt
from jwt import ExpiredSignatureError, DecodeError
from schemas.response.project_response import (
    ProjectShortInfoResponseSchema,
    GetAllProjectsResponseSchema
)


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.project_repository: ProjectRepository = ProjectRepository(db=db)

    async def get_all(self, access_token: str | None) -> GetAllProjectsResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            projects = await self.project_repository.get_all(user_id=user_id)
            projects_response = [ProjectShortInfoResponseSchema.model_validate(project) for project in projects]
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
