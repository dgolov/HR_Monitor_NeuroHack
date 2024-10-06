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


@router.get("/hire-time")
async def hire_time(
    recruiter_name: str | None = None,
    recruiter_id: int | None = None,
    date_start: datetime | None = None,
    date_end: datetime | None = None,
    repository: Repository = repo_dep,
    page: str = "1",
    offset: str | None = None,
) -> list[schemas.HireTimeMetrics]:
    """Время закрытия вакансии по рекрутеру за период."""
    return await repository.get_hire_time_data(recruiter_name, date_start, date_end, recruiter_id, page, offset)


@router.get("/screen-time")
async def screen_time(
    recruiter_name: str | None = None,
    recruiter_id: int | None = None,
    date_start: datetime | None = None,
    date_end: datetime | None = None,
    page: str = "1",
    offset: str | None = None,
    repository: Repository = repo_dep,
) -> list[schemas.ScreenTimeMetrics]:
    """Скорость скрининга по рекрутеру за период."""
    return await repository.get_screen_time_data(recruiter_name, date_start, date_end, recruiter_id, page, offset)


@router.get("/hire-quality")
async def hire_quality(
    recruiter_name: str | None = None,
    recruiter_id: int | None = None,
    date_start: datetime | None = None,
    date_end: datetime | None = None,
    page: str = "1",
    offset: str | None = None,
    repository: Repository = repo_dep,
) -> list[schemas.HireQualityMetrics]:
    """Качество найма по рекрутеру за период.

    Считается как средняя стоимость закрытия вакансии деленная на кол-во отработанных дней сотрудником.
    """
    return await repository.get_hire_quality_data(recruiter_name, date_start, date_end, recruiter_id, page, offset)


@router.get("/manager-satisfaction")
async def owner_satisfaction(
    recruiter_name: str | None = None,
    recruiter_id: int | None = None,
    date_start: datetime | None = None,
    date_end: datetime | None = None,
    page: str = "1",
    offset: str | None = None,
    repository: Repository = repo_dep,
) -> list[schemas.OwnerSatisfaction]:
    """Удовлетворенность менеджеров команд качеством сотрудников, по рекрутеру за период.

    Считается как средняя оценка тимлидом работы сотрудников по итогам месяца.
    """
    return await repository.get_owner_satisfaction(recruiter_name, date_start, date_end, recruiter_id, page, offset)


@router.get("/average-manager-satisfaction")
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
                "average_satisfaction_level": round(average_rating, 2),
            }

    recruiter_data = {
        recruiter_name: schemas.RecruiterMonthlyRatings(month_data=dict(months_data))
        for recruiter_name, months_data in response_data.items()
    }

    return schemas.RecruiterRatingsResponse(recruiter_data=recruiter_data)


@router.get("/vacancy-cost")
async def vacancy_cost(
    recruiter_name: str | None = None,
    recruiter_id: int | None = None,
    date_start: datetime | None = None,
    date_end: datetime | None = None,
    page: str = "1",
    offset: str | None = None,
    repository: Repository = repo_dep,
) -> list[schemas.VacancyCostMetrics]:
    """Средняя стоимость закрытия вакансии по рекрутеру за период."""
    return await repository.get_vacancy_cost_data(recruiter_name, date_start, date_end, recruiter_id, page, offset)


@router.get("/vacancy-cost-comparison")
async def vacancy_cost_comparison(
    recruiter_name: str | None = None,
    recruiter_id: int | None = None,
    date_start: datetime | None = None,
    date_end: datetime | None = None,
    page: str = "1",
    offset: str | None = None,
    repository: Repository = repo_dep,
) -> list[schemas.VacancyCostMetricsComparison]:
    """Сравнение стоимости закрытия вакансии по рефералу и без, по рекрутеру за период."""
    return await repository.get_vacancy_cost_comparison_data(
        recruiter_name, date_start, date_end, recruiter_id, page, offset
    )


@router.get("/avarage-vacancy-cost")
async def avarage_vacancy_cost(
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
    for vacancy in closed_vacancies:
        if vacancy.close_at:
            year = vacancy.close_at.year
            month = vacancy.close_at.month
            recruiter_id = int(vacancy.recruiter_id)

            recruiter = await repository.get_user_by_id(recruiter_id)
            recruiter_salary = recruiter.salary
            recruiter_name = recruiter.name

            grouped_data[recruiter_name][year][month]["total_salary"] = recruiter_salary
            grouped_data[recruiter_name][year][month]["vacancies_count"] += 1

    for recruiter_name in grouped_data:
        for year in grouped_data[recruiter_name]:
            for month in grouped_data[recruiter_name][year]:
                grouped_data[recruiter_name][year][month]["vacancy_cost"] = (
                    grouped_data[recruiter_name][year][month]["total_salary"]
                    / grouped_data[recruiter_name][year][month]["vacancies_count"]
                )
    return grouped_data


@router.get("/referal-part")
async def referal_count(
    recruiter_id: str | None = None,
    date_start: datetime | None = None,
    date_end: datetime | None = None,
    repository: Repository = repo_dep,
) -> schemas.ReferralCountResponse:
    """Кол-во кандидатов, которые были найдены по рефералу и без, за период."""
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
    """Соотношение трудоустроенных кандидатов к отклоненным за период."""
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
    total_candidates_count = len(hired_candidates) + len(rejected_candidates)

    return schemas.HiredRejectedResponse(
        total_count=total_candidates_count,
        hired_count=len(hired_candidates),
        rejected_count=len(rejected_candidates),
    )


@router.get("/hired-to-fired")
async def hired_to_fired(
    recruiter_id: str | None = None,
    date_start: datetime | None = None,
    date_end: datetime | None = None,
    repository: Repository = repo_dep,
) -> schemas.Hired2Fired:
    """Соотношение трудоустроенных кандидатов к уволенным за период."""
    hired_candidates = await repository.get_candidates(
        vacancy_id=None,
        status="hired",
        recruiter_id=recruiter_id,
        date_start=date_start,
        date_end=date_end,
    )
    fired_employees = await repository.get_fired_employees(
        recruiter_id=recruiter_id,
        date_start=date_start,
        date_end=date_end,
    )

    return schemas.Hired2Fired(
        hired_count=len(hired_candidates),
        fired_count=len(fired_employees),
    )


@router.get("/less6month-fired")
async def get_fired_employees_count(
    date_start: datetime,
    date_end: datetime,
    repository: Repository = repo_dep,
) -> schemas.EmployeeCountResponse:
    """Кол-во сотрудников, проработавших менее 6 месяцев за период."""
    fired_employees = await repository.get_fired_employees(date_end, date_start)

    count_fired_less_than_6_months = sum(
        (employee.date_fired - employee.date_started).days < 6 * 30 for employee in fired_employees
    )

    return schemas.EmployeeCountResponse(
        total_fired_less_than_6_months=count_fired_less_than_6_months,
    )


@router.get("/3year-fired")
async def get_fired_employees_for_last_3_years(
    repository: Repository = repo_dep,
    recruiter_id: int | None = None,
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
                recruiter_id,
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


@router.get("/average-candidate-to-vacancy")
async def get_average_candidate_to_vacancy(
    reference_date: datetime,
    repository: Repository = repo_dep,
) -> dict[str, float]:
    """Среднне кол-во откликов на закрытую вокансии за 6 месяцев от референс_дэйт."""
    six_months_ago = reference_date - timedelta(days=6 * 30)
    all_recruiters = await repository.get_all_recruiters()
    average_replays_vacancy_by_recruiter = {}

    for recruiter in all_recruiters:
        closed_vacancies_last_six_month = await repository.get_vacancies(
            date_start=six_months_ago,
            date_end=reference_date,
            recruiter_id=recruiter.id,
        )

        all_candidates = [
            len(await repository.get_candidates(vacancy_id=vacancy.id)) for vacancy in closed_vacancies_last_six_month
        ]
        try:
            average_candidate_to_vacancy = sum(all_candidates) / len(closed_vacancies_last_six_month)
        except ZeroDivisionError:
            average_candidate_to_vacancy = 0
        average_replays_vacancy_by_recruiter[recruiter.name] = average_candidate_to_vacancy

    return average_replays_vacancy_by_recruiter


@router.get("/average-candidate-to-vacancy-history")
async def get_average_candidate_to_vacancy_history(
    recruiter_name: str | None = None,
    recruiter_id: int | None = None,
    date_start: datetime | None = None,
    date_end: datetime | None = None,
    page: str = "1",
    offset: str | None = None,
    repository: Repository = repo_dep,
) -> list[schemas.HireTimeMetrics]:
    """Время закрытия вакансии по рекрутеру за период."""
    return await repository.get_average_candidate_to_vacancy(
        recruiter_name, date_start, date_end, recruiter_id, page, offset
    )
