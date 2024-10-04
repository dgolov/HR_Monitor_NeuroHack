from fastapi import FastAPI
from src.api.base_route import router as base_router


def create_app():
    application = FastAPI()
    application.include_router(base_router)
    return application
