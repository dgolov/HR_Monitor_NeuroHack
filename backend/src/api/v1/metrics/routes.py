from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import APIRouter

from src.api.v1.deps import repo_dep
from src.repositiry.repo import Repository
from src.schema import schemas


router = APIRouter(prefix="/metrics")


@router.get("/average-hire-time")
async def average_hire_time(
        recruiter_id: int | None = None,
        date_start: datetime | None = None,
        date_end: datetime | None = None,
        repository: Repository = repo_dep,
) -> schemas.VacancyAverageTimeResponse:
    """Среднее время закрытия вакансии по годам и месяцам."""
    vacancies = await repository.get_grouped_vacancies(
        recruiter_id=recruiter_id,
        date_start=date_start,
        date_end=date_end,
    )
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


@router.get("/screen-time")
async def screen_time(
        recruiter_name: str | None = None,
        date_start: datetime | None = None,
        date_end: datetime | None = None,
        repository: Repository = repo_dep,
) -> list[schemas.ScreenTimeMetrics]:
    """Скорость скрининга по рекрутеру за период."""
    return await repository.get_screen_time_data(recruiter_name, date_start, date_end)


@router.get("/hire-quality")
async def hire_quality(
        recruiter_name: str | None = None,
        date_start: datetime | None = None,
        date_end: datetime | None = None,
        repository: Repository = repo_dep,
) -> list[schemas.HireQualityMetrics]:
    """Качество найма по рекрутеру за период.

    Считается как средняя стоимость закрытия вакансии деленная на кол-во отработанных дней сотрудником.
    """
    return await repository.get_hire_quality_data(recruiter_name, date_start, date_end)


@router.get("/vacancy-cost")
async def vacancy_cost(
        recruiter_id: int | None = None,
        date_start: datetime | None = None,
        date_end: datetime | None = None,
        repository: Repository = repo_dep,
) -> dict:
    """Средняя стоимость закрытия вакансий по годам и месяцам.

    Пример ответа:
    {
  "Tiffany Woods": {
    "2024": {
      "1": {
        "total_salary": 3839,
        "vacancies_count": 3,
        "vacancy_cost": 1279.6666666666667
      },
      "2": {
        "total_salary": 3839,
        "vacancies_count": 4,
        "vacancy_cost": 959.75
      },
      "4": {
        "total_salary": 3839,
        "vacancies_count": 3,
        "vacancy_cost": 1279.6666666666667
      },
      "5": {
        "total_salary": 3839,
        "vacancies_count": 3,
        "vacancy_cost": 1279.6666666666667
      },...
    """
    closed_vacancies = await repository.get_vacancies(
        status="closed",
        creator_id=None,
        recruiter_id=recruiter_id,
        date_start=date_start,
        date_end=date_end,
    )
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
    recruiters_ids = []
    for vacancy in closed_vacancies:
        if vacancy.close_at:  # Проверяем, что дата закрытия существует
            year = vacancy.close_at.year
            month = vacancy.close_at.month
            recruiter_id = int(vacancy.recruiter_id)

            recruiter = await repository.get_user_by_id(recruiter_id)
            recruiter_salary = recruiter.salary
            recruiter_name = recruiter.name

            # Обновляем сумму зарплат и количество вакансий
            grouped_data[recruiter_name][year][month]["total_salary"] = recruiter_salary
            grouped_data[recruiter_name][year][month]["vacancies_count"] += 1

    for recruiter_name in grouped_data:
        for year in grouped_data[recruiter_name]:
            for month in grouped_data[recruiter_name][year]:
                grouped_data[recruiter_name][year][month]["vacancy_cost"] = grouped_data[recruiter_name][year][month][
                                                                              "total_salary"] / \
                                                                          grouped_data[recruiter_name][year][month][
                                                                              "vacancies_count"]
    return grouped_data


@router.get("/referal-part")
async def referal_count(
        recruiter_id: str | None = None,
        date_start: datetime | None = None,
        date_end: datetime | None = None,
        repository: Repository = repo_dep,
) -> schemas.ReferralCountResponse:
    """Кол-во кандидатов, которые были найдены по рефералу за период."""
    hired_candidates = await repository.get_candidates(
        vacancy_id=None,
        status="hired",
        recruiter_id=recruiter_id,
        date_start=date_start,
        date_end=date_end,
    )
    total_hired = len(hired_candidates)
    referral_count = sum(1 for candidate in hired_candidates if candidate.is_referral)
    non_referral_count = total_hired - referral_count

    return schemas.ReferralCountResponse(
        total_hired=total_hired,
        referral_count=referral_count,
        non_referral_count=non_referral_count,
    )


@router.get("/hired-to-rejected")
async def hired_to_rejected(
        recruiter_id: str | None = None,
        date_start: datetime | None = None,
        date_end: datetime | None = None,
        repository: Repository = repo_dep,
) -> schemas.HiredRejectedResponse:
    """Соотношение всех кандидатов к трудоустроенным и отклоненных за период."""
    hired_candidates = await repository.get_candidates(
        vacancy_id=None,
        status="hired",
        recruiter_id=recruiter_id,
        date_start=date_start,
        date_end=date_end,
    )
    rejected_candidates = await repository.get_candidates(
        vacancy_id=None,
        status="rejected",
        recruiter_id=recruiter_id,
        date_start=date_start,
        date_end=date_end,
    )
    total_hired = len(hired_candidates) + len(rejected_candidates)

    return schemas.HiredRejectedResponse(
        total_count=total_hired,
        hired_count=len(hired_candidates),
        rejected_count=len(rejected_candidates),
    )


@router.get("/soon-fired")
async def get_fired_employees_count(
        reference_date: datetime,
        repository: Repository = repo_dep,
):
    # Вычисляем дату 6 месяцев назад от заданной даты
    six_months_ago = reference_date - timedelta(days=6 * 30)
    # Запрос для получения сотрудников, уволенных за последние 6 месяцев

    fired_employees = await repository.get_fired_employees(reference_date, six_months_ago)

    # Подсчитываем тех, кто проработал менее 6 месяцев
    count_fired_less_than_6_months = sum(
        (employee.date_fired - employee.date_started).days < 6 * 30 for employee in fired_employees
    )

    return schemas.EmployeeCountResponse(
        total_fired_less_than_6_months=count_fired_less_than_6_months,
    )


@router.get("/soon_fired_summary")
async def get_fired_employees_for_last_3_years(
        repository: Repository = repo_dep,
):
    current_date = datetime.now()

    summary = defaultdict(lambda: defaultdict(dict))

    for year_offset in range(3):
        year = current_date.year - year_offset
        for month in range(1, 13):
            first_day_of_month = datetime(year, month, 1)

            if first_day_of_month > current_date:
                continue

            first_day_next_month = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

            six_months_ago = first_day_of_month - timedelta(days=6 * 30)

            fired_employees = await repository.get_fired_employees_by_month(
                first_day_of_month,
                first_day_next_month,
                six_months_ago,
            )

            count_fired_less_than_6_months = sum(
                1
                for employee in fired_employees
                if employee.date_started and (employee.date_fired - employee.date_started).days < 6 * 30
            )

            summary[year][month] = {
                "count_fired_less_than_6_months": count_fired_less_than_6_months,
            }

    return summary


@router.get("/average_manager_rating")
async def get_average_manager_rating(
        year: int,
        repository: Repository = repo_dep,
) -> schemas.RecruiterRatingsResponse:
    # Определяем границы заданного года
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    employees = await repository.get_employees_by_started_date(start_date, end_date)

    # Группируем данные по рекрутерам и месяцам
    data = defaultdict(lambda: defaultdict(list))

    for employee, recruiter_name in employees:
        month = employee.date_started.month
        data[recruiter_name][month].append(employee.manager_rating)

    # Рассчитываем средний рейтинг по месяцам для каждого рекрутера
    response_data = defaultdict(lambda: defaultdict(dict))
    for recruiter_name, months_data in data.items():
        for month, ratings in months_data.items():
            average_rating = sum(ratings) / len(ratings) if ratings else 0
            response_data[recruiter_name][month] = {
                "average_satisfaction_level": round(average_rating, 2)
            }

    recruiter_data = {
        recruiter_name: schemas.RecruiterMonthlyRatings(month_data=dict(months_data))
        for recruiter_name, months_data in response_data.items()
    }

    return schemas.RecruiterRatingsResponse(recruiter_data=recruiter_data)
