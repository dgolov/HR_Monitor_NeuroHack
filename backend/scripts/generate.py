import os
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
from dotenv import load_dotenv
from src.database.models import Base, Candidate, Vacancy, VacancyFile, User, Interview, RecruiterTask


load_dotenv()
fake = Faker()


DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def create_candidate():
    return Candidate(
        uuid=uuid4(),
        name=fake.name(),
        is_referral=random.choice([True, False]),
        other_info={"hobbies": fake.words(3), "experience": fake.job()},
        resume_link=fake.url(),
        status=random.choice(["applied", "interviewed", "hired"]),
        vacancy_id=random.randint(1, 10)
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
        creator_id=random.randint(1, 5)
    )


def create_vacancy_file():
    return VacancyFile(
        uuid=uuid4(),
        name=fake.file_name(),
        description=fake.text(),
        link=fake.url(),
        created_at=fake.date_this_year()
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
        is_active=True
    )


def create_interview(candidate_id, recruiter_id):
    return Interview(
        uuid=uuid4(),
        title=fake.catch_phrase(),
        description=fake.text(),
        candidate_id=1,
        type=random.choice(["tech", "HR"]),
        recruiter_id=1,
        tech_id=1,
        status=random.choice(["scheduled", "completed", "canceled"]),
        other_info={"notes": fake.paragraph()},
        created_at=fake.date_this_year(),
        date_start_at=fake.date_this_year(),
        date_end_at=fake.date_this_year()
    )


def create_recruiter_task(recruiter_id):
    return RecruiterTask(
        uuid=uuid4(),
        type=random.choice(["interview", "screening", "follow-up"]),
        recruiter_id=recruiter_id,
        description=fake.text(),
        status=random.choice(["open","pending", "completed"]),
        priority=random.randint(1, 5),
        created_at=fake.date_this_year(),
        started_at=fake.date_this_year(),
        closed_at=fake.date_this_year()
    )


def populate_database():
    for _ in range(10):
        session.add(create_candidate())

    for _ in range(5):
        session.add(create_vacancy())

    for _ in range(5):
        session.add(create_vacancy_file())

    recruiters = []
    for _ in range(3):
        user = create_user()
        session.add(user)
        recruiters.append(user)

    for _ in range(5):
        candidate_id = random.randint(1, 10)
        recruiter_id = random.choice(recruiters).id
        session.add(create_interview(candidate_id, recruiter_id))

    for recruiter in recruiters:
        session.add(create_recruiter_task(recruiter.id))

    session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    populate_database()
    print("Данные успешно сгенерированы и записаны в базу!")
