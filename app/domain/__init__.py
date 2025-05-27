from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient

from app.api import bonus


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.mongo_client = AsyncIOMotorClient("mongodb://dev:devpas@localhost:27017/")
    yield
    app.state.mongo_client.close()


def create_app() -> FastAPI:
    app = FastAPI(title="Bonus Calculation API", lifespan=lifespan)

    app.include_router(bonus.router, prefix="/api", tags=["Bonus"])

    return app
