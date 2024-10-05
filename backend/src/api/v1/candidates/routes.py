from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.api.v1.deps import repo_dep
from src.repositiry.repo import Repository
from src.schema import schemas
from src.settings import logger
from src.database import models


router = APIRouter(prefix="/candidates")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_candidate(
    data: schemas.CandidateCreate,
    repository: Repository = repo_dep,
) -> JSONResponse:
    logger.debug(f"Create candidate - {data}")
    await repository.create_candidate(candidate=data)
    return JSONResponse(
        content={"message": "Ok"},
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/candidates/{vacancy_id}")
async def get_candidates(
        vacancy_id: int
):
    log.debug(f'route /candidates/ called with {vacancy_id=}')
    candidates_list: List[models.Candidate] = await repository.get_candidates(vacancy_id=vacancy_id)
    return list(schemas.Candidate.from_orm(candidate) for candidate in candidates_list)
