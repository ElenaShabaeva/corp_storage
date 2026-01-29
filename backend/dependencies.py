from fastapi import Depends
from services.user_service import UserService
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db=db)
