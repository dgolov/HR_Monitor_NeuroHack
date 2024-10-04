from fastapi import FastAPI
from backend.api.base_route import router as base_router


def create_app():
    application = FastAPI()
    application.include_router(base_router)
    return application
