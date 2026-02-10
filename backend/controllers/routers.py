from fastapi import APIRouter
from controllers.user_controller import router as user_router
from controllers.project_controller import router as project_router


router = APIRouter()

router.include_router(user_router)
router.include_router(project_router)
