from fastapi import APIRouter, status, Query
from fastapi.responses import JSONResponse
from src.api.v1.deps import repo_dep
from src.schema import schemas
from src.repositiry.repo import Repository
from src.settings import logger
from datetime import datetime


router = APIRouter(prefix="/vacancies")


@router.post("/")
async def create_vacancy(
        data: schemas.VacancyCreate,
        repository: Repository = repo_dep
):
    logger.debug(f'Create vacancy - {data}')
    await repository.create_vacancy(vacancy=data)
    return JSONResponse(
        content={"message": "Ok"},
        status_code=status.HTTP_201_CREATED
    )


@router.get("/")
async def get_vacancies(
        candidate_id: int = Query(None),
        type: str = Query(None),
        recruiter_id: int = Query(None),
        status: str = Query(None),
        created_from: datetime = Query(None),
        created_before: datetime = Query(None),
):
    log.debug(f'get vacancies called with {candidate_id=}, {type=}, {recruiter_id=}, {status=}, {created_from},'
              f'{created_before=}')
    # todo
