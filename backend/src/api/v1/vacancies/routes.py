from datetime import datetime

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from src.api.v1.deps import repo_dep
from src.repositiry.repo import Repository
from src.schema import schemas
from src.settings import logger


router = APIRouter(prefix="/vacancies")


@router.post("/")
async def create_vacancy(
    data: schemas.VacancyCreate,
    repository: Repository = repo_dep,
):
    logger.debug(f"Create vacancy - {data}")
    await repository.create_vacancy(vacancy=data)
    return JSONResponse(
        content={"message": "Ok"},
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/")
async def get_vacancies(
    candidate_id: int | None = Query(None),
    type: str | None = Query(None),
    recruiter_id: int | None = Query(None),
    status: str | None = Query(None),
    created_from: datetime | None = Query(None),
    created_before: datetime | None = Query(None),
) -> list[schemas.Vacancy]:
    logger.debug(
        f"get vacancies called with {candidate_id=}, {type=}, {recruiter_id=}, {status=}, {created_from},"
        f"{created_before=}",
    )
    # TODO
