from fastapi import APIRouter
from src.routes import users, plans, reports

router = APIRouter()
router.include_router(users.router)
router.include_router(plans.router)
router.include_router(reports.router)
