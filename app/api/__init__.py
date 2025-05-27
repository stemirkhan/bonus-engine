from fastapi import APIRouter

from .bonus import router as bonus_router

router = APIRouter()



router.include_router(bonus_router, prefix="/bonus", tags=["Bonus"])
