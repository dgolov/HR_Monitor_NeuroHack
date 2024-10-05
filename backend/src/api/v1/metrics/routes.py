from collections import defaultdict

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
                "vacancies_count": 0,
            }

        grouped_data[year][month]["total_closure_time"] += closure_time
        grouped_data[year][month]["vacancies_count"] += 1

    average_data = {}
    for year, months in grouped_data.items():
        average_data[year] = {}
        for month, data in months.items():
            average_closure_time = data["total_closure_time"] / data["vacancies_count"]
            average_data[year][month] = schemas.MonthData(
                average_closure_time_in_days=average_closure_time,
                vacancies_count=data["vacancies_count"],
            )

    return schemas.VacancyAverageTimeResponse(data=average_data)


@router.get("screen-time")
async def screen_time(repository: Repository = repo_dep) -> list[schemas.ScreenTimeMetrics]:
    screen_time_data = await repository.get_screen_time_data()
    return [schemas.ScreenTimeMetrics.model_validate(recruiter) for recruiter in screen_time_data]


@router.get("/hire-quality")
async def hire_quality(repository: Repository = repo_dep) -> list[schemas.HireQualityMetrics]:
    hire_quality_data = await repository.get_hire_quality_data()
    return [schemas.HireQualityMetrics.model_validate(recruiter) for recruiter in hire_quality_data]


@router.get("/vacancy_cost")
async def vacancy_cost(repository: Repository = repo_dep):
    """Пример ответа {
    "2024": {
        "1": {
            "average_vacancy_cost": 1500.0
        },
        "2": {
            "average_vacancy_cost": 1200.0
        }
    },
    "2023": {
        "12": {
            "average_vacancy_cost": 1800.0
        }
    }
    }.
    """
    closed_vacancies = await repository.get_vacancies(status="closed", creator_id=None)
    grouped_data = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(
                lambda: {
                    "total_salary": 0,
                    "vacancies_count": 0,
                },
            ),
        ),
    )

    for vacancy in closed_vacancies:
        if vacancy.close_at:  # Проверяем, что дата закрытия существует
            year = vacancy.close_at.year
            month = vacancy.close_at.month
            recruiter_id = vacancy.recruiter_id

            # Получаем зарплату рекрутера (предполагается, что вы можете получить её через объект User)
            recruiter_salary = await repository.get_user_salary(recruiter_id)

            # Обновляем сумму зарплат и количество вакансий
            grouped_data[recruiter_id][year][month]["total_salary"] += recruiter_salary
            grouped_data[recruiter_id][year][month]["vacancies_count"] += 1

    # Подсчет средней зарплаты по месяцам
    average_data = defaultdict(lambda: defaultdict(dict))

    for recruiter_id, years in grouped_data.items():
        for year, months in years.items():
            for month, data in months.items():
                total_salary = data["total_salary"]
                vacancies_count = data["vacancies_count"]

                if vacancies_count > 0:
                    average_salary = total_salary / vacancies_count
                    average_data[year][month] = {
                        "average_vacancy_cost": average_salary,
                    }

    return dict(average_data)
