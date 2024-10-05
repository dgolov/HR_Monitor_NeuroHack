from fastapi import APIRouter

from src.api.v1.deps import repo_dep
from src.repositiry.repo import Repository
from src.schema import schemas


router = APIRouter(prefix="/metrics")


@router.get("/average_hire_time")
async def average_hire_time(repository: Repository = repo_dep) -> schemas.VacancyAverageTimeResponse:
    # Группируем вакансии по году и месяцу закрытия

    grouped_vacancies = await repository.get_grouped_vacancies
    result = {}
    for entry in grouped_vacancies:
        year = entry.year
        month = entry.month

        # Если год ещё не в словаре, добавляем
        if year not in result:
            result[year] = {}

        # Добавляем данные по месяцам
        result[year][month] = {
            "average_closure_time_in_days": entry.average_closure_time,
            "vacancies_count": entry.vacancies_count,
        }

    return schemas.VacancyAverageTimeListResponse(data=result)
