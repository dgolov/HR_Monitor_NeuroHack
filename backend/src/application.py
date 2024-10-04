import logging

from fastapi import FastAPI
from src.api.base_route import router as base_router
import os


def create_app():
    application = FastAPI()
    application.include_router(base_router)
    return application


if not os.path.exists('../logs'):
    os.makedirs('../logs')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/app.log"),
        logging.StreamHandler()
    ]
)

log = logging.getLogger(__name__)
log.info('app started')
