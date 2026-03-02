from database.database import Base
from sqlalchemy import Column, String, func, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class RefreshToken(Base):
    __tablename__ = "refresh_token"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
    token_hash = Column(String, nullable=False, unique=True)
    jti = Column(UUID(as_uuid=True), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="refresh_tokens")
