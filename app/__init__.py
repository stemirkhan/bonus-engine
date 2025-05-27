from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api import router
from app.api.exception_handlers import bonus_exception_handler
from app.exceptions import BonusCalculationBaseError
from app.db.mongo import mongo_client, mongo_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.mongo_client = mongo_client
    app.state.mongo_db = mongo_db
    try:
        yield
    finally:
        mongo_client.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Bonus Calculation API",
        lifespan=lifespan,
    )

    app.include_router(router, prefix="/api/v1", tags=["Bonus"])

    app.add_exception_handler(BonusCalculationBaseError, bonus_exception_handler)

    return app
