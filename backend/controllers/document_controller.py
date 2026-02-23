from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from configuration import settings
from services.document_service import DocumentService
from uuid import UUID


router = APIRouter(
    prefix="/project",
    tags=["Document"]
)


@router.post("/{project_id}/documents")
async def create_document(
        project_id: UUID,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        document_service: DocumentService = Depends(DocumentService)
):
    return await document_service.create_document(project_id=project_id, access_token=credentials.credentials)
