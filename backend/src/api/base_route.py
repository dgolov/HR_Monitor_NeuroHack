from fastapi import APIRouter

from src.api.v1 import candidates_routes, interviews_routes, user_routes, vacancies_routes, vacancy_files_routes
from src.settings import logger


router = APIRouter()

router.include_router(candidates_routes.router, tags=["candidates"])
router.include_router(interviews_routes.router, tags=["interviews"])
router.include_router(user_routes.router, tags=["users"])
router.include_router(vacancies_routes.router, tags=["vacancies"])
router.include_router(vacancy_files_routes.router, tags=["vacancy_files"])


@router.get("/health")
def health_check() -> dict:
    logger.debug("healthcheck")
    return {"message": "Server is running"}
