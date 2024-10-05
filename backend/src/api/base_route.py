from fastapi import APIRouter

from src.api.v1 import (
    candidates_routes,
    interviews_routes,
    metrics_routes,
    user_routes,
    vacancies_routes,
    vacancy_files_routes,
)
from src.settings import logger
from src.scripts.generate import generate_bd


router = APIRouter()

router.include_router(candidates_routes.router, tags=["candidates"])
router.include_router(interviews_routes.router, tags=["interviews"])
router.include_router(user_routes.router, tags=["users"])
router.include_router(vacancies_routes.router, tags=["vacancies"])
router.include_router(vacancy_files_routes.router, tags=["vacancy_files"])
router.include_router(metrics_routes.router, tags=["metrics"])


@router.get("/health")
def health_check() -> dict:
    logger.debug("healthcheck")
    return {"message": "Server is running"}


@router.get("/init_random_db")
async def generate_db() -> dict:
    logger.info('Starting DB randomize')
    await generate_bd()
    return {"message": "DB generated"}
