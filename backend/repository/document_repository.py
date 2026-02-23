from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.document import Document
from uuid import UUID
from datetime import datetime


class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def post(
            self,
            project_id: UUID,
            creator_id: UUID,
            file_path: str,
            created_at: datetime
    ) -> Document:
        document_db = Document(
            file_path=file_path,
            created_at=created_at,
            project_id=project_id,
            creator_id=creator_id
        )

        self._db.add(document_db)
        await self._db.flush()
        return document_db
