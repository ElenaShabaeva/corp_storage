from fastapi import Depends
from services.user_service import UserService
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.project_service import ProjectService


def get_user_service():
    return UserService()


def get_project_service():
    return ProjectService()
