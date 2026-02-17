from database.database import Base
from sqlalchemy import Column, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    name = Column(String(length=150), nullable=False)
    surname = Column(String(length=150), nullable=False)
    login = Column(String(length=16), nullable=False, unique=True)
    password = Column(String(length=16), nullable=False)

    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    project_association = relationship("UserProjectAssociation", back_populates="user")
    created_projects = relationship("Project", back_populates="creator", cascade="all, delete-orphan")
    sent_invites = relationship(
        "InviteNotification",
        foreign_keys="InviteNotification.from_user_id",
        back_populates="from_user",
        cascade="all, delete-orphan"
    )
    received_invites = relationship(
        "InviteNotification",
        foreign_keys="InviteNotification.to_user_id",
        back_populates="to_user",
        cascade="all, delete-orphan"
    )
    sent_messages = relationship(
        "MessageNotification",
        foreign_keys="MessageNotification.from_user_id",
        back_populates="from_user",
        cascade="all, delete-orphan"
    )
    receive_messages = relationship(
        "MessageNotification",
        foreign_keys="MessageNotification.to_user_id",
        back_populates="to_user",
        cascade="all, delete-orphan"
    )
