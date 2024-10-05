from datetime import datetime

from fastapi import APIRouter

from src.api.v1.deps import repo_dep
from src.repositiry.repo import Repository
from src.schema import schemas


router = APIRouter(prefix="/tasks")


@router.get("/")
async def get_task(
        start: datetime,
        end: datetime,
        status: str,
        repository: Repository = repo_dep,
) -> list[schemas.RecruiterTask]:
    tasks_list = await repository.get_tasks(start, end, status)
    return [schemas.RecruiterTask.model_validate(task) for task in tasks_list]


@router.get("/{recruiter_id}")
async def get_task(
        recruiter_id: int,
        start: datetime,
        end: datetime,
        status: str,
        repository: Repository = repo_dep,
) -> list[schemas.RecruiterTask]:
    tasks_list = await repository.get_tasks_by_hr_id(start, end, status, recruiter_id)
    return [schemas.RecruiterTask.model_validate(task) for task in tasks_list]
