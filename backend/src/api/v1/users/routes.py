from fastapi import APIRouter, status, Query
from fastapi.responses import JSONResponse
from src.api.v1.deps import repo_dep
from src.schema import schemas
from src.repositiry.repo import Repository
from src.settings import logger


router = APIRouter(prefix="/users")


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


@router.get('/{user_id}')
async def get_user(
        user_id: int,
        role: str = Query(None),
):
    logger.debug(f'get user by id {user_id}, role={role}')
    pass  # todo
