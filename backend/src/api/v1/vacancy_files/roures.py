from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.api.v1.deps import repo_dep
from src.schema import schemas
from src.repositiry.repo import Repository


router = APIRouter(prefix="/vacancy_files")


@router.post("/")
async def create_vacancy_file(
        data: schemas.VacancyFileCreate,
        repository: Repository = repo_dep
):
    await repository.create_vacancy_file(vacancy_file=data)
    return JSONResponse(
        content={"message": "Ok"},
        status_code=status.HTTP_201_CREATED
    )
