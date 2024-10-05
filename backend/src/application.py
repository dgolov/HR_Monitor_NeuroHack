from fastapi import FastAPI

from src.api.base_route import router as base_router
from src.settings import logger


def create_app() -> FastAPI:
    logger.info("Start backend")
    application = FastAPI()
    application.include_router(base_router)
    return application
