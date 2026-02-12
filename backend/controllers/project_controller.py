from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from configuration import settings
from services.project_service import ProjectService
from uuid import UUID
from schemas.request.project_request import (
    ProjectCreateRequestSchema
)
from schemas.response.project_response import (
    GetAllProjectsResponseSchema,
    ProjectShortInfoResponseSchema,
    ProjectFullInfoResponseSchema
)


router = APIRouter(
    prefix="/project",
    tags=["Project"]
)


@router.get("/all", response_model=GetAllProjectsResponseSchema)
async def get_all(
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        project_service: ProjectService = Depends(ProjectService)
):
    return await project_service.get_all(access_token=credentials.credentials)


@router.post("", response_model=ProjectShortInfoResponseSchema)
async def create(
        payload: ProjectCreateRequestSchema,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        project_service: ProjectService = Depends(ProjectService)
):
    return await project_service.create(payload=payload, access_token=credentials.credentials)


@router.get("/{id}")
async def get_by_id(
        project_id: UUID,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        project_service: ProjectService = Depends(ProjectService)
):
    return await project_service.get_by_id(project_id=project_id, access_token=credentials.credentials)
