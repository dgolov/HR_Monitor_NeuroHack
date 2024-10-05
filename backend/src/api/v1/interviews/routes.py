from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.api.v1.deps import repo_dep
from src.schema import schemas
from src.repositiry.repo import Repository
from src.settings import logger


router = APIRouter(prefix="/interviews")


@router.post("/")
async def create_interview(
        data: schemas.InterviewCreate,
        repository: Repository = repo_dep
):
    logger.debug(f'Create interview - {data}')
    await repository.create_interview(interview=data)
    return JSONResponse(
        content={"message": "Ok"},
        status_code=status.HTTP_201_CREATED
    )
