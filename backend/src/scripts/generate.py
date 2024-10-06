import datetime as dt
import random
from datetime import timedelta
from uuid import uuid4

from faker import Faker
from sqlalchemy import select

from src.database.db import async_session_maker
from src.database.models import (
    Candidate,
    Employee,
    HireQualityMetrics,
    Interview,
    RecruiterTask,
    ScreenTimeMetrics,
    User,
    Vacancy,
    VacancyFile, OwnerSatisfactionMetrics, AverageCandidateToVacancyMetrics, VacancyCostMetrics,
    VacancyCostComparisonMetrics, HireTimeMetrics,
)
from src.settings import logger

fake = Faker()

session = async_session_maker()

CLOSED_VACANCIES = []


def create_candidate(vacancy_id, is_referal, vacancy_status):
    if vacancy_status == 'closed' and vacancy_id not in CLOSED_VACANCIES:
        status = 'hired'
        CLOSED_VACANCIES.append(vacancy_id)
    elif vacancy_status in ["open", "in progress"]:
        status = random.choice(["applied", "interviewed", "rejected", "rejected", "rejected"])
    else:
        status = 'rejected'

    return Candidate(
        uuid=uuid4(),
        name=fake.name(),
        is_referral=is_referal if status == 'hired' else random.choice(
            [True, False, False, False, False, False, False]),
        other_info={"hobbies": fake.words(3), "experience": fake.job()},
        resume_link=fake.url(),
        status=status,
        vacancy_id=vacancy_id,
    )


def create_vacancy(recruiter_id: int, vacancy_file_id: int) -> Vacancy:
    created_at = fake.date_between(start_date='-3y', end_date='-1y')
    is_referral = random.choice([True, False, False, False, False])
    update_range = (1, 7) if is_referral else (10, 20)
    updated_at = created_at + timedelta(days=random.choice(list(range(*update_range))))
    closed_at = updated_at + timedelta(days=random.choice(list(range(10, 20))))
    closing_cost = (closed_at - created_at).days * 5000
    status = random.choice(["open", "closed", "in progress"])
    viewed_count = random.randint(0, 1000)
    responded_count = viewed_count - random.randint(0, 300) or 0

    if status != 'closed':
        closed_at = None
        closing_cost = None
        is_referral = None
    return Vacancy(
        uuid=uuid4(),
        title=fake.job(),
        description=fake.text(),
        status=status,
        created_at=created_at,
        open_at=created_at,
        updated_at=updated_at,
        close_at=closed_at,
        viewed_count=viewed_count,
        responded_count=responded_count,
        vacancy_file_id=vacancy_file_id,
        creator_id=recruiter_id,
        recruiter_id=recruiter_id,
        closing_cost=closing_cost,
        is_referral=is_referral
    )


def create_vacancy_file():
    return VacancyFile(
        uuid=uuid4(),
        name=fake.file_name(),
        description=fake.text(),
        link=fake.url(),
        created_at=fake.date_this_year(),
    )


def create_user(role: str):
    return User(
        uuid=uuid4(),
        password_hash=fake.sha256(),
        name=fake.name(),
        email=fake.email(),
        role=role,
        phone=fake.phone_number(),
        is_verified=random.choice([True, False]),
        is_active=True,
        salary=random.randrange(70000, 100000),
        grade=random.randrange(1, 5),
        efficiently=random.randrange(1, 5),
    )


def create_interview(candidate_id: int, recruiter_id: int, tech_id: int, status: str) -> Interview:
    created_at = fake.date_time_between(start_date='-3y', end_date='-1y')
    date_start_at = created_at + timedelta(days=random.randint(1, 7))
    date_end_at = date_start_at + timedelta(hours=random.randint(1, 3))
    if status in ['scheduled', 'canceled']:
        date_start_at = None
        date_end_at = None
    return Interview(
        uuid=uuid4(),
        title=fake.catch_phrase(),
        description=fake.text(),
        candidate_id=candidate_id,
        type=random.choice(["tech", "HR"]),
        recruiter_id=recruiter_id,
        tech_id=tech_id,
        status=status,  # scheduled, completed, canceled
        other_info={"notes": fake.paragraph()},
        created_at=created_at,
        date_start_at=date_start_at,
        date_end_at=date_end_at,
    )


def create_recruiter_task(recruiter_id: int) -> RecruiterTask:
    created_at = fake.date_between(start_date='-3y', end_date='-1y')
    started_at = created_at + timedelta(days=random.choice(list(range(1, 4))))
    closed_at = started_at + timedelta(days=random.choice(list(range(30, 80))))
    status = random.choice(["open", "pending", "completed"])
    if status != 'completed':
        closed_at = None
    return RecruiterTask(
        uuid=uuid4(),
        type=random.choice(["interview", "screening", "follow-up"]),
        recruiter_id=recruiter_id,
        description=fake.text(),
        status=random.choice(["open", "pending", "completed"]),
        priority=random.randint(1, 5),
        created_at=created_at,
        started_at=started_at,
        closed_at=closed_at,
    )


def create_hire_quality_metrics(recruiter_name):
    data = []
    for year in (2021, 2022, 2023):
        for month in (range(1, 13)):
            _date = dt.date(year, month, 1)
            data.append(HireQualityMetrics(
                recruiter_name=recruiter_name,
                month=_date,
                value=round(random.uniform(0, 1), 3),
            ))
    return data


def create_screen_time_metrics(recruiter_name):
    data = []
    for year in (2021, 2022, 2023):
        for month in (range(1, 13)):
            _date = dt.date(year, month, 1)
            data.append(ScreenTimeMetrics(
                recruiter_name=recruiter_name,
                month=_date,
                value=round(random.uniform(5.0, 10.0), 3)
            ))
    return data


def create_hire_time_metrics(recruiter_name):
    data = []
    for year in (2021, 2022, 2023):
        for month in (range(1, 13)):
            _date = dt.date(year, month, 1)
            data.append(HireTimeMetrics(
                recruiter_name=recruiter_name,
                month=_date,
                value=random.randint(15, 60)
            ))
    return data


def create_satisfaction_metrics(recruiter_name):
    data = []
    for year in (2021, 2022, 2023):
        for month in (range(1, 13)):
            _date = dt.date(year, month, 1)
            data.append(OwnerSatisfactionMetrics(
                recruiter_name=recruiter_name,
                month=_date,
                value=random.randint(1, 10)
            ))
    return data


def create_average_candidate_metrics(recruiter_name):
    data = []
    for year in (2021, 2022, 2023):
        for month in (range(1, 13)):
            _date = dt.date(year, month, 1)
            data.append(AverageCandidateToVacancyMetrics(
                recruiter_name=recruiter_name,
                month=_date,
                value=random.randint(1, 100)
            ))
    return data


def create_vacancy_cost_metrics(recruiter_name):
    data = []
    for year in (2021, 2022, 2023):
        for month in (range(1, 13)):
            _date = dt.date(year, month, 1)
            data.append(VacancyCostMetrics(
                recruiter_name=recruiter_name,
                month=_date,
                value=random.randint(15000, 30000)
            ))
    return data


def create_vacancy_cost_comparison_metrics(recruiter_name):
    data = []
    for year in (2021, 2022, 2023):
        for month in (range(1, 13)):
            for is_referral in (True, False):
                _date = dt.date(year, month, 1)
                data.append(VacancyCostComparisonMetrics(
                    recruiter_name=recruiter_name,
                    month=_date,
                    value=random.randint(5000, 15000) if is_referral else random.randint(15000, 30000),
                    is_referral=is_referral
                ))
    return data


def create_employee(recruiter_id):
    date_started = fake.date_between(start_date='-3y', end_date='-1y')
    date_fired = random.choice([date_started + timedelta(days=random.randint(1, 365)), None])

    return Employee(
        name=fake.name(),
        date_started=date_started,
        date_fired=date_fired,
        position=fake.job(),
        cost_of_hiring=random.randrange(15000, 80000),
        manager_rating=random.randint(1, 10),
        recruiter_id=recruiter_id,
    )


async def populate_database() -> None:
    recruiters = [create_user('recruiter') for _ in range(10)]
    session.add_all(recruiters)
    await session.commit()
    tech_specialists = [create_user('tech') for _ in range(10)]
    session.add_all(tech_specialists)
    await session.commit()

    vacancies = [create_vacancy(random.choice(recruiters).id, _) for _ in range(5000)]
    session.add_all(vacancies)
    await session.commit()

    query = await session.execute(select(Vacancy))
    vacancies = query.scalars().all()
    vacancy_ids = iter([(vacancy.id, vacancy.is_referral, vacancy.status) for vacancy in vacancies] * 5)
    candidates = [create_candidate(*next(vacancy_ids)) for _ in range(15000)]
    session.add_all(candidates)
    await session.commit()

    vacancy_files = [create_vacancy_file() for _ in range(5000)]
    session.add_all(vacancy_files)
    await session.commit()

    recruiters_tasks = [create_recruiter_task(random.choice(recruiters).id) for _ in range(5000)]
    session.add_all(recruiters_tasks)

    await session.commit()

    query = await session.execute(select(Candidate).filter(Candidate.status == 'hired'))
    hired_candidates = query.scalars().all()
    query = await session.execute(select(Vacancy))
    vacancies = query.scalars().all()

    vacancy_dict = {vacancy.id: vacancy.recruiter_id for vacancy in vacancies}
    interviews = [create_interview(candidate.id,
                                   vacancy_dict[candidate.vacancy_id],
                                   random.choice(tech_specialists).id,
                                   'completed') for candidate in hired_candidates]
    session.add_all(interviews)

    await session.commit()

    query = await session.execute(select(Candidate).filter(Candidate.status == 'applied'))
    applied_candidates = query.scalars().all()
    interviews = [create_interview(candidate.id,
                                   vacancy_dict[candidate.vacancy_id],
                                   random.choice(tech_specialists).id,
                                   random.choice(['scheduled', 'canceled'])) for candidate in applied_candidates]
    session.add_all(interviews)

    quality_metrics = []
    for recruiter in recruiters:
        quality_metrics.extend(create_hire_quality_metrics(recruiter.name))
    session.add_all(quality_metrics)

    screen_time_metrics = []
    for recruiter in recruiters:
        screen_time_metrics.extend(create_screen_time_metrics(recruiter.name))
    session.add_all(screen_time_metrics)

    hire_time_metrics = []
    for recruiter in recruiters:
        hire_time_metrics.extend(create_hire_time_metrics(recruiter.name))
    session.add_all(hire_time_metrics)

    owner_satisfaction = []
    for recruiter in recruiters:
        owner_satisfaction.extend(create_satisfaction_metrics(recruiter.name))
    session.add_all(owner_satisfaction)

    average_candidate_to_vacancy = []
    for recruiter in recruiters:
        average_candidate_to_vacancy.extend(create_average_candidate_metrics(recruiter.name))
    session.add_all(average_candidate_to_vacancy)

    vacancy_cost = []
    for recruiter in recruiters:
        vacancy_cost.extend(create_vacancy_cost_metrics(recruiter.name))
    session.add_all(vacancy_cost)

    vacancy_cost_comparison = []
    for recruiter in recruiters:
        vacancy_cost_comparison.extend(create_vacancy_cost_comparison_metrics(recruiter.name))
    session.add_all(vacancy_cost_comparison)

    employees = [create_employee(random.choice(recruiters).id) for _ in range(5000)]
    session.add_all(employees)

    await session.commit()


async def generate_bd() -> None:
    await populate_database()
    logger.info("Database populated successfully.")
    await session.close()
