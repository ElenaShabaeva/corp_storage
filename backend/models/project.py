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


class Project(Base):
    __tablename__ = "project"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    name = Column(String(length=65))
    description = Column(String(length=200))
    members_count = Column(Integer)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))

    creator = relationship("User", back_populates="created_projects")
    user_association = relationship("UserProjectAssociation", back_populates="project")
