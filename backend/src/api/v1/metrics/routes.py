from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.api.v1.deps import repo_dep
from src.schema import schemas
from src.repositiry.repo import Repository
from src.settings import logger


router = APIRouter(prefix="/metrics")


@app.get("/vacancies/average_hire_time")
def average_hire_time(repository: Repository = repo_dep):
    # Группируем вакансии по году и месяцу закрытия

    grouped_vacancies = repo_dep.get_grouped_vacancies
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
            "vacancies_count": entry.vacancies_count
        }

    return schemas.VacancyAverageTimeListResponse(data=result)
