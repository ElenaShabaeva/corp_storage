from database.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    Integer,
    func,
    ForeignKey
)


class UserProjectAssociation(Base):
    __tablename__ = "user_project_association"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="project_association")
    project = relationship("Project", back_populates="user_association")
