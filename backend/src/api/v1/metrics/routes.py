from fastapi import APIRouter

from src.api.v1.deps import repo_dep
from src.repositiry.repo import Repository
from src.schema import schemas


router = APIRouter(prefix="/metrics")


@router.get("/average-hire-time")
async def average_hire_time(repository: Repository = repo_dep) -> schemas.VacancyAverageTimeResponse:

    vacancies = await repository.get_grouped_vacancies()
    grouped_data = {}

    for vacancy in vacancies:
        year = vacancy.close_at.year
        month = vacancy.close_at.month

        closure_time = (vacancy.close_at - vacancy.open_at).days

        if year not in grouped_data:
            grouped_data[year] = {}

        if month not in grouped_data[year]:
            grouped_data[year][month] = {
                "total_closure_time": 0,
                "vacancies_count": 0
            }

        grouped_data[year][month]["total_closure_time"] += closure_time
        grouped_data[year][month]["vacancies_count"] += 1

    average_data = {}
    for year, months in grouped_data.items():
        average_data[year] = {}
        for month, data in months.items():
            average_closure_time = data["total_closure_time"] / data["vacancies_count"]
            average_data[year][month] = MonthData(
                average_closure_time_in_days=average_closure_time,
                vacancies_count=data["vacancies_count"]
            )

    return schemas.VacancyAverageTimeResponse(data=average_data)


@router.get("screen-time")
async def screen_time(repository: Repository = repo_dep) -> list[schemas.ScreenTimeMetrics]:
    screen_time_data = await repository.get_screen_time_data()

    return [recruiter.dict() for recruiter in screen_time_data]
