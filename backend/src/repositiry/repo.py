from datetime import datetime
from typing import Any, List, Optional

from fastapi import HTTPException
from sqlalchemy import Select, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import models
from src.schema import schemas
from src.settings import logger


class RepositoryBase:
    """Базовый класс обращения в БД."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _all(self, query: Select) -> list[Any]:
        query_result = await self.session.execute(query)
        rows = query_result.all()
        return [data[0] for data in rows if data[0]]

    async def _first(self, query):
        query_result = await self.session.execute(query)
        result = query_result.first()
        if result:
            return result[0]
        return None

    @staticmethod
    async def _one(result):
        return result.one()

    async def _insert_one(self, model: Any) -> None:
        try:
            self.session.add(model)
            await self.session.commit()
        except Exception as e:
            logger.error(f"Add {model.__tablename__} error - {e}")
            raise HTTPException(status_code=400, detail="Bad request") from e

    async def _update(self, obj, data) -> None:
        if not isinstance(data, dict):
            data = data.dict()
        for field, value in data.items():
            setattr(obj, field, value)
        await self.session.commit()

    async def _delete(self, obj) -> None:
        await self.session.delete(obj)
        await self.session.commit()

    @staticmethod
    async def _query_offset(query, offset: int, page: int = 1):
        if not page:
            return query
        page = max(page, 1)
        return query.limit(offset).offset(offset * (page - 1))


class Repository(RepositoryBase):
    user = models.User
    vacancy = models.Vacancy
    vacancy_file = models.VacancyFile
    interview = models.Interview
    candidate = models.Candidate
    screen_time = models.ScreenTimeMetrics
    hire_quality = models.HireQualityMetrics

    async def get_users(self, role: Optional[str] = None) -> List[models.User]:
        query = select(self.user)
        if role:
            query = query.where(self.user.role == role)
        return await self._all(query=query)

    async def get_user_by_id(self, user_id: int) -> models.User:
        user = await self.session.get(self.user, user_id)
        if not user:
            logger.warning(f"User {user_id} is not found")
            raise HTTPException(status_code=404, detail="Not found")
        return user

    async def create_user(self, user: schemas.UserCreate) -> None:
        user_model = models.User(**user.model_dump())
        await self._insert_one(user_model)

    async def get_user_salary(self, user_id: int) -> int:
        user = await self.get_user_by_id(user_id)
        return int(user.salary) if user else 0

    async def get_vacancies(
        self,
        creator_id: Optional[int] = None,
        status: Optional[str] = None,
        filter_by: Optional[dict[str, Any]] = None,
    ) -> List[models.Vacancy]:
        query = select(self.vacancy)
        if creator_id:
            query = query.where(self.vacancy.creator_id == creator_id)
        if status:
            query = query.where(self.vacancy.status == status)
        if filter_by:
            filters = {key: value for key, value in filter_by.items() if value}
            query = query.filter_by(**filters)
        return await self._all(query=query)

    async def get_vacancy_by_id(self, vacancy_id: int) -> models.Vacancy:
        vacancy = await self.session.get(self.vacancy, vacancy_id)
        if not vacancy:
            logger.warning(f"Vacancy {vacancy_id} is not found")
            raise HTTPException(status_code=404, detail="Not found")
        return vacancy

    async def create_vacancy(self, vacancy: schemas.VacancyCreate) -> None:
        vacancy_model = models.Vacancy(**vacancy.model_dump())
        await self._insert_one(vacancy_model)

    async def get_vacancy_files(self) -> List[models.VacancyFile]:
        query = select(self.vacancy_file)
        return await self._all(query=query)

    async def get_vacancy_file_by_id(self, vacancy_file_id: int) -> models.VacancyFile:
        vacancy_file = await self.session.get(self.vacancy_file, vacancy_file_id)
        if not vacancy_file:
            logger.warning(f"Vacancy file {vacancy_file_id} is not found")
            raise HTTPException(status_code=404, detail="Not found")
        return vacancy_file

    async def create_vacancy_file(self, vacancy_file: schemas.VacancyFileCreate) -> None:
        vacancy_file_model = models.VacancyFile(**vacancy_file.model_dump())
        await self._insert_one(vacancy_file_model)

    async def get_interviews(self, candidate_id: int, status: str) -> List[models.Interview]:
        query = select(self.interview)
        if candidate_id:
            query = query.where(self.interview.candidate_id == candidate_id)
        if status:
            query = query.where(self.interview.status == status)
        return await self._all(query=query)

    async def get_interview_by_id(self, interview_id: int) -> models.Interview:
        query = select(self.interview).where(self.interview.id == interview_id)
        interview = await self._one(query)
        if not interview:
            logger.warning(f"Interview {interview_id} is not found")
            raise HTTPException(status_code=404, detail="Not found")
        return interview

    async def create_interview(self, interview: schemas.InterviewCreate) -> None:
        interview_model = models.Interview(**interview.model_dump())
        await self._insert_one(interview_model)

    async def get_candidates(
        self,
        vacancy_id: Optional[int] = None,
        status: Optional[str] = None,
        recruiter_id: str | None = None,
        date_start: datetime | None = None,
        date_end: datetime | None = None,
    ) -> list[models.Candidate]:
        query = select(self.candidate)
        if vacancy_id:
            query = query.where(self.candidate.vacancy_id == vacancy_id)
        if status:
            query = query.where(self.candidate.status == status)
        if recruiter_id:
            query = query.join(self.vacancy).join(self.user).where(self.user.id == int(recruiter_id))
            if date_start and date_end:
                query = query.where(
                    and_(
                        self.vacancy.created_at >= date_start,
                        self.vacancy.created_at <= date_end,
                    ),
                )

        elif date_start and date_end:
            query = query.join(self.vacancy).where(
                and_(
                    self.vacancy.created_at >= date_start,
                    self.vacancy.created_at <= date_end,
                ),
            )
        return await self._all(query=query)

    async def get_candidate_by_id(self, candidate_id: int) -> models.Candidate:
        candidate = await self.session.get(self.candidate, candidate_id)
        if not candidate:
            logger.warning(f"Candidate {candidate_id} is not found")
            raise HTTPException(status_code=404, detail="Not found")
        return candidate

    async def create_candidate(self, candidate: schemas.CandidateCreate) -> None:
        candidate_model = models.Candidate(**candidate.model_dump())
        await self._insert_one(candidate_model)

    async def get_grouped_vacancies(self) -> List[models.Vacancy]:
        query = select(models.Vacancy).filter(
            models.Vacancy.status == "closed",
            models.Vacancy.close_at.isnot(None),
            models.Vacancy.open_at.isnot(None),
        )
        return await self._all(query=query)

    async def get_screen_time_data(
        self,
        recruiter_name: str | None,
        date_start: datetime | None,
        date_end: datetime | None,
    ) -> List[models.ScreenTimeMetrics]:
        query = select(self.screen_time)
        if recruiter_name:
            query = query.where(self.screen_time.recruiter_name == recruiter_name)
        if date_start and date_end:
            query = query.where(
                and_(
                    self.screen_time.month >= date_start,
                    self.screen_time.month <= date_end,
                ),
            )
        return await self._all(query=query)

    async def get_hire_quality_data(
        self,
        recruiter_name: str | None,
        date_start: datetime | None,
        date_end: datetime | None,
    ) -> List[models.HireQualityMetrics]:
        query = select(self.hire_quality)
        if recruiter_name:
            query = query.where(self.hire_quality.recruiter_name == recruiter_name)
        if date_start and date_end:
            query = query.where(
                and_(
                    self.hire_quality.month >= date_start,
                    self.hire_quality.month <= date_end,
                ),
            )
        return await self._all(query=query)

    async def get_fired_employees(self, reference_date: datetime, six_months_ago: datetime) -> List[models.Employee]:
        query = select(models.Employee).filter(
            and_(
                models.Employee.date_fired >= six_months_ago,
                models.Employee.date_fired <= reference_date,
            ),
        )
        return await self._all(query=query)

    async def get_fired_employees_by_month(
        self,
        first_day_of_month: datetime,
        first_day_next_month: datetime,
        six_months_ago: datetime,
    ) -> List[models.Employee]:
        query = select(models.Employee).filter(
            and_(
                models.Employee.date_fired >= first_day_of_month,
                models.Employee.date_fired < first_day_next_month,
                models.Employee.date_fired >= six_months_ago,
            ),
        )
        return await self._all(query=query)
