from fastapi import HTTPException, status
from utils.uow import UnitOfWork
from uuid import UUID, uuid4
from utils.jwt_utils import decode_jwt
from jwt import ExpiredSignatureError, DecodeError
from pathlib import Path
from docx import Document
from datetime import datetime
from schemas.response.document_response import DocumentResponseSchema


class DocumentService:
    def __init__(self):
        self.uow: UnitOfWork = UnitOfWork()

    async def create_document(self, access_token: str | None, project_id: UUID):
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)

            async with self.uow.start():
                members = await self.uow.projects.get_members(project_id=project_id)
                user = await self.uow.users.get_by_id(user_id=user_id)

                if user not in members:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Нет прав"
                    )

                project = await self.uow.projects.get_by_id(project_id=project_id)
                if not project:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Проект не найден"
                    )
                new_document = Document()
                filename = f"{uuid4()}.docx"
                file_path = Path("storage/documents") / str(project.id) / filename
                file_path.parent.mkdir(parents=True, exist_ok=True)
                new_document.save(str(file_path))
                created_at = datetime.now()

                document_db = await self.uow.documents.post(
                    file_path=str(file_path),
                    created_at=created_at,
                    project_id=project.id,
                    creator_id=user.id
                )
            return DocumentResponseSchema(
                id=document_db.id,
                file_path=str(document_db.file_path),
                project_id=document_db.project_id,
                creator_id=document_db.creator_id,
                created_at=document_db.created_at.strftime("%d.%m.%Y / %H:%M")
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
