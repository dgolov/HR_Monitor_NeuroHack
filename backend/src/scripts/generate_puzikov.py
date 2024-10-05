import os
import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from src.database.models import Candidate, Vacancy, VacancyFile, User, Interview, RecruiterTask, ScreenTimeMetrics, HireQualityMetrics, Base
import asyncio

fake = Faker()

# Создание асинхронного подключения к базе данных
DATABASE_URL = os.getenv('DATABASE_URL')  # Обновите на свои данные
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def generate_candidates(num, vacancy_ids):
    candidates = []
    for _ in range(num):
        candidates.append(
            Candidate(
                name=fake.name(),
                is_referral=random.choice([True, False]),
                other_info={"skills": fake.words(random.randint(2, 5))},
                resume_link=fake.url(),
                status=random.choice(['applied', 'interviewed', 'hired', 'rejected']),
                vacancy_id=random.choice(vacancy_ids)  # Замените на реальный диапазон ID вакансий
            )
        )
    return candidates

async def generate_vacancies(num, user_ids, vacancy_ids):
    vacancies = []
    for _ in range(num):
        created_at = fake.date_between(start_date='-3y', end_date='-1y')
        closed_at = created_at + timedelta(days=random.choice(list(range(30, 80))))
        vacancies.append(
            Vacancy(
                title=fake.job(),
                description=fake.text(),
                status=random.choice(['open', 'closed']),
                created_at=created_at,
                open_at=created_at,
                updated_at=closed_at,
                close_at=closed_at,
                viewed_count=random.randint(0, 100),
                responded_count=random.randint(0, 50),
                vacancy_file_id=random.choice(vacancy_ids),  # Замените на реальный диапазон ID файлов вакансий
                creator_id=random.choice(user_ids),  # Замените на реальный диапазон ID создателей
                recruiter_id=random.choice(user_ids)  # Замените на реальный диапазон ID рекрутеров
            )
        )
    return vacancies

async def generate_vacancy_files(num):
    vacancy_files = []
    for _ in range(num):
        vacancy_files.append(
            VacancyFile(
                name=fake.file_name(),
                description=fake.text(),
                link=fake.url(),
                created_at=fake.date_between(start_date='-1y', end_date='today')
            )
        )
    return vacancy_files

async def generate_users(num):
    users = []
    for _ in range(num):
        users.append(
            User(
                password_hash=fake.sha256(),
                name=fake.name(),
                email=fake.unique.email(),
                role=random.choice(['recruiter', 'admin']),
                phone=fake.phone_number(),
                is_verified=random.choice([True, False]),
                is_active=random.choice([True, False]),
                salary=random.randint(30000, 120000)
            )
        )
    return users

async def generate_interviews(num, user_ids):
    interviews = []
    for _ in range(num):
        interviews.append(
            Interview(
                title=fake.catch_phrase(),
                description=fake.text(),
                candidate_id=random.choice(user_ids),  # Замените на реальный диапазон ID кандидатов
                type=random.choice(['phone', 'on-site', 'video']),
                recruiter_id=random.choice(user_ids),  # Замените на реальный диапазон ID рекрутеров
                tech_id=random.choice(user_ids),  # Замените на реальный диапазон ID технарей
                status=random.choice(['scheduled', 'completed', 'canceled']),
                other_info={"notes": fake.text()},
                created_at=fake.date_between(start_date='-1y', end_date='today'),
                date_start_at=fake.date_time_this_year(),
                date_end_at=fake.date_time_this_year() + timedelta(hours=random.randint(1, 3))
            )
        )
    return interviews

async def generate_recruiter_tasks(num):
    tasks = []
    for _ in range(num):
        tasks.append(
            RecruiterTask(
                uuid=uuid4(),
                type=random.choice(['follow-up', 'screening', 'interview']),
                recruiter_id=random.randint(1, num-1),  # Замените на реальный диапазон ID рекрутеров
                description=fake.text(),
                status=random.choice(['pending', 'in progress', 'completed']),
                priority=random.randint(1, 5),
                created_at=fake.date_between(start_date='-1y', end_date='today'),
                started_at=fake.date_this_year(),
                closed_at=fake.date_between(start_date='today', end_date='+1y')
            )
        )
    return tasks

async def generate_screen_time_metrics(num):
    metrics = []
    for _ in range(num):
        metrics.append(
            ScreenTimeMetrics(
                recruiter_name=fake.name(),
                month=fake.date_this_month(),
                value=random.uniform(0, 8)
            )
        )
    return metrics

async def generate_hire_quality_metrics(num):
    metrics = []
    for _ in range(num):
        metrics.append(
            HireQualityMetrics(
                recruiter_name=fake.name(),
                month=fake.date_this_month(),
                value=random.uniform(0, 1)
            )
        )
    return metrics

async def main():
    await create_db()

    async with AsyncSessionLocal() as session:
        num_records = 100  # Количество записей для генерации
        users = await generate_users(num_records)
        tasks = await generate_recruiter_tasks(num_records)
        screen_time_metrics = await generate_screen_time_metrics(num_records)
        hire_quality_metrics = await generate_hire_quality_metrics(num_records)

        # Сохранение данных в базу
        session.add_all(users)
        await session.commit()
        user_ids = [user.id for user in users]  # Получаем ID пользователей
        print(user_ids)
        vacancy_files = await generate_vacancy_files(num_records)
        vacancy_file_ids = [vacancy_file.id for vacancy_file in vacancy_files]
        vacancies = await generate_vacancies(300, user_ids, vacancy_file_ids)
        session.add_all(vacancies)
        await session.commit()
        session.add_all(vacancy_files)
        await session.commit()
        vacancy_ids = [vacancy.id for vacancy in vacancies]
        candidates = await generate_candidates(num_records, vacancy_ids)

        session.add_all(candidates)
        await session.commit()
        interviews = await generate_interviews(num_records, user_ids)

        session.add_all(interviews)
        await session.commit()

        session.add_all(tasks)
        await session.commit()

        session.add_all(screen_time_metrics)
        await session.commit()

        session.add_all(hire_quality_metrics)
        await session.commit()

        await session.commit()


# Запуск асинхронного процесса
asyncio.run(main())
