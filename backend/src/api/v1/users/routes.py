from fastapi import APIRouter, status, Query
from fastapi.responses import JSONResponse
from src.api.v1.deps import repo_dep
from src.database import models
from src.schema import schemas
from src.repositiry.repo import Repository
from src.settings import logger
from typing import List


router = APIRouter(prefix="/users")


@router.get("/")
async def get_users(repository: Repository = repo_dep) -> List[schemas.User]:
    users_list: List[models.User] = await repository.get_users()
    return list(schemas.User.from_orm(user) for user in users_list)


@router.post("/")
async def create_user(
        data: schemas.UserCreate,
        repository: Repository = repo_dep
):
    logger.debug(f'Create user - {data}')
    await repository.create_user(user=data)
    return JSONResponse(
        content={"message": "Ok"},
        status_code=status.HTTP_201_CREATED
    )
