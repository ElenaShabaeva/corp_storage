from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from uuid import UUID
from models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def post(
            self,
            token_hash: str,
            expires_at: datetime,
            user_id: UUID
    ) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at
        )
        self.db.add(refresh_token)
        await self.db.commit()
        await self.db.refresh(refresh_token)
        return refresh_token
