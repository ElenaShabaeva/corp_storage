from fastapi import APIRouter, Depends, WebSocket, Query
from fastapi.security import HTTPAuthorizationCredentials
from configuration import settings
from services.document_service import DocumentService
from uuid import UUID
from schemas.response.document_response import (
    DocumentResponseSchema,
    DocumentResponseSchema,
    DocumentsResponseSchema
)
from schemas.response.standart_message import MessageResponseSchema


router = APIRouter(
    prefix="/project",
    tags=["Document"]
)


@router.post("/{project_id}/documents", response_model=DocumentResponseSchema)
async def create_document(
        project_id: UUID,
        file_name: str,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        document_service: DocumentService = Depends(DocumentService)
):
    return await document_service.create_document(
        project_id=project_id,
        access_token=credentials.credentials,
        filename=file_name
    )


@router.get("/{project_id}/documents/all", response_model=DocumentsResponseSchema)
async def get_all(
        project_id: UUID,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        document_service: DocumentService = Depends(DocumentService)
):
    return await document_service.get_all(project_id=project_id, access_token=credentials.credentials)


@router.delete("/{project_id}/documents", response_model=MessageResponseSchema)
async def delete(
        project_id: UUID,
        document_id: UUID,
        credentials: HTTPAuthorizationCredentials = Depends(settings.http_bearer),
        document_service: DocumentService = Depends(DocumentService)
):
    return await document_service.delete(
        access_token=credentials.credentials,
        project_id=project_id,
        document_id=document_id
    )


@router.websocket("/documents/ws/{document_id}")
async def connect(
        websocket: WebSocket,
        document_id: UUID,
        token: str = Query(...),
        document_service: DocumentService = Depends(DocumentService)
):
    access_token = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )
    await document_service.connect(
        access_token=access_token.credentials,
        document_id=document_id,
        websocket=websocket
    )
