from database.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy import (
    Column,
    DateTime,
    String,
    func,
    ForeignKey
)


class Document(Base):
    __tablename__ = "document"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    filename = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    yjs_updates = Column(BYTEA, nullable=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    project = relationship("Project", back_populates="documents")
    creator = relationship("User", back_populates="created_documents")
