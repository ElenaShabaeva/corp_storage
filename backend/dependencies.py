from fastapi import Depends
from services.user_service import UserService
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.project_service import ProjectService


def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db=db)


def get_project_service(db: AsyncSession = Depends(get_db)):
    return ProjectService(db=db)
