from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from configuration import settings
from dependencies import get_project_service
from services.project_service import ProjectService


router = APIRouter(
    prefix="/project",
    tags=["Project"]
)


@router.get("/all")
async def get_all(
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        project_service: ProjectService = Depends(get_project_service)
):
    return await project_service.get_all(access_token=credentials.credentials)
