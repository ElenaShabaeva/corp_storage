from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from models.user import User
from uuid import UUID


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_login(self, login: str) -> User | None:
        result = await self.db.execute(select(User).where(User.login == login))
        return result.scalar_one_or_none()

    async def post(
            self,
            name: str,
            surname: str,
            login: str,
            password: str
    ) -> User:
        user = User(
            name=name,
            surname=surname,
            login=login,
            password=password
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def patch(self, updated_user: User) -> User:
        self.db.add(updated_user)
        await self.db.flush()
        await self.db.refresh(updated_user)
        return updated_user

    async def delete(self, user_id: UUID):
        result = await self.db.execute(
            delete(User)
            .where(User.id == user_id)
        )
        return result.rowcount
