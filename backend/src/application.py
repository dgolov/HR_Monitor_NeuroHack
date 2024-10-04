import logging

from fastapi import FastAPI
from src.api.base_route import router as base_router


def create_app():
    application = FastAPI()
    application.include_router(base_router)
    return application


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

log = logging.getLogger(__name__)
