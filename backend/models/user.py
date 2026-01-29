from database.database import Base
from sqlalchemy import Column, String, func
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    name = Column(String)
    surname = Column(String)
    login = Column(String)
    password = Column(String)
