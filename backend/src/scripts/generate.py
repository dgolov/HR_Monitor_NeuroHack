import random
from datetime import datetime, timedelta
from uuid import uuid4

from faker import Faker

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
    VacancyFile,
)
from src.settings import logger


fake = Faker()

session = async_session_maker()


def create_candidate():
    return Candidate(
        uuid=uuid4(),
        name=fake.name(),
        is_referral=random.choice([True, False]),
        other_info={"hobbies": fake.words(3), "experience": fake.job()},
        resume_link=fake.url(),
        status=random.choice(["applied", "interviewed", "hired"]),
        vacancy_id=random.randint(1, 10),
    )


def create_vacancy():
    return Vacancy(
        uuid=uuid4(),
        title=fake.job(),
        description=fake.text(),
        status=random.choice(["open", "closed", "in progress"]),
        created_at=fake.date_this_year(),
        open_at=fake.date_this_year(),
        updated_at=fake.date_this_year(),
        close_at=fake.date_this_year(),
        viewed_count=random.randint(0, 100),
        responded_count=random.randint(0, 100),
        vacancy_file_id=random.randint(1, 10),
        creator_id=random.randint(1, 5),
        recruiter_id=random.randint(1, 5),
    )


def create_vacancy_file():
    return VacancyFile(
        uuid=uuid4(),
        name=fake.file_name(),
        description=fake.text(),
        link=fake.url(),
        created_at=fake.date_this_year(),
    )


def create_user():
    return User(
        uuid=uuid4(),
        password_hash=fake.sha256(),
        name=fake.name(),
        email=fake.email(),
        role=random.choice(["recruiter", "admin", "developer"]),
        phone=fake.phone_number(),
        is_verified=random.choice([True, False]),
        is_active=True,
        salary=random.randrange(2000, 5000),
    )


def create_interview(candidate_id, recruiter_id, tech_id):
    return Interview(
        uuid=uuid4(),
        title=fake.catch_phrase(),
        description=fake.text(),
        candidate_id=candidate_id,
        type=random.choice(["tech", "HR"]),
        recruiter_id=recruiter_id,
        tech_id=tech_id,
        status=random.choice(["scheduled", "completed", "canceled"]),
        other_info={"notes": fake.paragraph()},
        created_at=fake.date_this_year(),
        date_start_at=fake.date_this_year(),
        date_end_at=fake.date_this_year(),
    )


def create_recruiter_task(recruiter_id):
    return RecruiterTask(
        uuid=uuid4(),
        type=random.choice(["interview", "screening", "follow-up"]),
        recruiter_id=recruiter_id,
        description=fake.text(),
        status=random.choice(["open", "pending", "completed"]),
        priority=random.randint(1, 5),
        created_at=fake.date_this_year(),
        started_at=fake.date_this_year(),
        closed_at=fake.date_this_year(),
    )


def create_hire_quality_metrics(recruiter_name):
    return HireQualityMetrics(
        recruiter_name=recruiter_name,
        month=fake.date_between(datetime(2024, 1, 1), datetime.now()),
        value=round(random.uniform(0, 1), 3),
    )


def create_screen_time_metrics(recruiter_name):
    return ScreenTimeMetrics(
        recruiter_name=recruiter_name,
        month=fake.date_between(datetime(2024, 1, 1), datetime.now()),
        value=round(random.uniform(0, 1), 3),
    )


def create_employee():
    return Employee(
        name=fake.name(),
        date_started=fake.date_between(datetime(2023, 1, 1), datetime.now() - timedelta(days=365)),
        date_fired=fake.date_between(datetime(2024, 1, 1), datetime.now()),
        position=fake.catch_phrase(),
        cost_of_hiring=random.randrange(100, 400),
        manager_rating=random.randint(1, 6),
        recruiter_id=random.randint(1, 5),
    )


async def populate_database() -> None:
    recruiters = [create_user() for _ in range(10)]
    session.add_all(recruiters)
    await session.commit()

    for _ in range(10000):
        session.add(create_vacancy())
    await session.commit()

    for _ in range(10000):
        session.add(create_candidate())
    await session.commit()

    for _ in range(5):
        session.add(create_vacancy_file())
    await session.commit()

    for _ in range(6):
        for i in range(1, 5):
            session.add(create_recruiter_task(i))

    await session.commit()

    for _ in range(5):
        candidate_id = random.randint(1, 10)
        recruiter = random.choice(recruiters)
        tech_id = random.randint(1, 10)
        session.add(create_interview(candidate_id, recruiter.id, tech_id))

    for _ in range(4000):
        session.add(create_hire_quality_metrics(recruiter.name))

    for _ in range(4000):
        recruiter = random.choice(recruiters)
        session.add(create_screen_time_metrics(recruiter.name))

    for _ in range(100):
        session.add(create_employee())

    await session.commit()


async def generate_bd() -> None:
    await populate_database()
    logger.info("Database populated successfully.")
    await session.close()
