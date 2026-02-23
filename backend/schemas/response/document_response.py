from pydantic import BaseModel
from uuid import UUID


# class DocumentResponseSchema(BaseModel):
#     id: UUID
#     file_path: str
#     project_id: UUID
#     creator_id: UUID
#     created_at: str


class DocumentResponseSchema(BaseModel):
    id: UUID
    name: str
    creator: str
    can_delete: bool


class DocumentsResponseSchema(BaseModel):
    count: int
    documents: list[DocumentResponseSchema]
