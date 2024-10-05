from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.api.v1.deps import repo_dep
from src.repositiry.repo import Repository
from src.schema import schemas
from src.settings import logger


router = APIRouter(prefix="/users")


@router.get("/")
async def get_users(repository: Repository = repo_dep) -> list[schemas.User]:
    users_list = await repository.get_users()
    return [schemas.User.model_validate(user) for user in users_list]


@router.post("/")
async def create_user(
    data: schemas.UserCreate,
    repository: Repository = repo_dep,
) -> JSONResponse:
    logger.debug(f"Create user - {data}")
    await repository.create_user(user=data)
    return JSONResponse(
        content={"message": "Ok"},
        status_code=status.HTTP_201_CREATED,
    )
