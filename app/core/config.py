import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    PROJECT_NAME: str = "My FastAPI Service"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    MONGO_URI: str
    MONGO_DB_NAME: str = "bonus"

    class Config:
        env_file = ".env"


class DevConfig(BaseConfig):
    DEBUG: bool = True

    class Config:
        env_file = ".env.dev"


class TestConfig(BaseConfig):
    DEBUG: bool = True

    class Config:
        env_file = ".env.test"


class ProdConfig(BaseConfig):
    DEBUG: bool = False

    class Config:
        env_file = ".env.prod"


@lru_cache()
def get_settings() -> BaseConfig:
    env = os.getenv("ENVIRONMENT", "dev").lower()
    if env == "prod":
        return ProdConfig()
    elif env == "test":
        return TestConfig()
    return DevConfig()


settings = get_settings()
