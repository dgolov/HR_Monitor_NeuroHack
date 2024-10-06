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
) -> JSONResponse:
    logger.debug(f"Create vacancy - {data}")
    await repository.create_vacancy(vacancy=data)
    return JSONResponse(
        content={"message": "Ok"},
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/")
async def get_vacancies(
    vtype: str | None = Query(None),
    recruiter_id: int | None = Query(None),
    status: str | None = Query(None),
    page: str | None = "1",
    offset: int | None = None,
    repository: Repository = repo_dep,
) -> list[schemas.Vacancy]:
    logger.debug(
        f"get vacancies called with {vtype=}, {recruiter_id=}, {status=}",
    )
    page=int(page)
    return await repository.get_vacancies(
        filter_by={
            "type": vtype,
            "recruiter_id": recruiter_id,
            "status": status,
        },
        page=page,
        offset=offset
    )
