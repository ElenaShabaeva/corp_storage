from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from uuid import UUID
from models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def post(
            self,
            token_hash: str,
            jti: UUID,
            expires_at: datetime,
            user_id: UUID
    ) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            jti=jti,
            token_hash=token_hash,
            expires_at=expires_at
        )
        self.db.add(refresh_token)
        await self.db.commit()
        await self.db.refresh(refresh_token)
        return refresh_token

    async def get_by_jti(self, jti: UUID) -> RefreshToken | None:
        result = await self.db.execute(
            select(RefreshToken)
            .where(RefreshToken.jti == jti)
            .where(RefreshToken.expires_at > datetime.now(timezone.utc))
            .where(RefreshToken.revoked_at.is_(None))
        )

        refresh_token = result.scalar_one_or_none()
        return refresh_token

    async def set_revoked_at(self, refresh_token: RefreshToken):
        refresh_token.revoked_at = datetime.now(timezone.utc)
        self.db.add(refresh_token)
        await self.db.commit()
