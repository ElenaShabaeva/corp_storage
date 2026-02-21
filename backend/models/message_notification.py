from database.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    DateTime,
    String,
    Boolean,
    func,
    ForeignKey
)


class MessageNotification(Base):
    __tablename__ = "message_notification"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    message = Column(String, nullable=False)
    message_datetime = Column(DateTime, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    from_user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
    to_user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))

    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_messages")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_messages")
