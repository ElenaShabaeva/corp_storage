from database.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from schemas.internal.invite_status_enum import InviteStatus
from sqlalchemy import (
    Column,
    Enum,
    DateTime,
    String,
    func,
    ForeignKey
)


class InviteNotification(Base):
    __tablename__ = "invite_notification"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    state = Column(Enum(InviteStatus), nullable=False, default=InviteStatus.SENT)
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    invite_datetime = Column(DateTime, nullable=False)
    from_user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    to_user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_invites")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_invites")
    project = relationship("Project", back_populates="invites")
