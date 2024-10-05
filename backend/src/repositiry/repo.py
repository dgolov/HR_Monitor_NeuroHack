from src.database import models
from src.schema import schemas
from src.settings import logger
from fastapi import HTTPException
from sqlalchemy import select
from typing import List, Optional


class RepositoryBase:
    """ Базовый класс обращения в БД """
    def __init__(self, session):
        self.session = session

    async def _all(self, query):
        query_result = await self.session.execute(query)
        rows = query_result.all()
        return [data[0] for data in rows if data[0]]

    async def _first(self, query):
        query_result = await self.session.execute(query)
        result = query_result.first()
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    async def _one(result):
        return result.one()

    async def _insert_one(self, model: models.Base) -> None:
        try:
            self.session.add(model)
            await self.session.commit()
        except Exception as e:
            logger.error(f"Add {model.__tablename__} error - {e}")
            raise HTTPException(status_code=400, detail="Bad request")

    async def _update(self, obj, data):
        if not isinstance(data, dict):
            data = data.dict()
        for field, value in data.items():
            setattr(obj, field, value)
        await self.session.commit()

    async def _delete(self, obj):
        await self.session.delete(obj)
        await self.session.commit()

    @staticmethod
    async def _query_offset(query, offset: int, page: int = 1):
        if not page:
            return query
        if page < 1:
            page = 1
        return query.limit(offset).offset(offset * (page - 1))


class Repository(RepositoryBase):
    user = models.User
    vacancy = models.Vacancy
    vacancy_file = models.VacancyFile
    interview = models.Interview
    candidate = models.Candidate

    async def get_users(self, role: Optional[str] = None) -> List[models.User]:
        query = select(self.user)
        if role:
            query = query.where(self.user.role == role)
        return await self._all(query=query)

    async def get_user_by_id(self, user_id: int) -> models.User:
        user: models.User = self.session.get(self.user, user_id)
        if not user:
            logger.warning(f"User {user_id} is not found")
            raise HTTPException(status_code=404, detail="Not found")
        return user

    async def create_user(self, user: schemas.UserCreate):
        user_model = models.User(**user.model_dump())
        self.session.add(user_model)
        await self.session.commit()

    async def get_vacancies(
            self, creator_id: Optional[int], status: Optional[str]
    ) -> List[models.Vacancy]:
        query = select(self.vacancy)
        if creator_id:
            query = query.where(self.vacancy.creator_id == creator_id)
        if status:
            query = query.where(self.vacancy.status == status)
        return await self._all(query=query)

    async def get_vacancy_by_id(self, vacancy_id: int) -> models.Vacancy:
        vacancy: models.Vacancy = self.session.get(self.vacancy, vacancy_id)
        if not vacancy:
            logger.warning(f"Vacancy {vacancy_id} is not found")
            raise HTTPException(status_code=404, detail="Not found")
        return vacancy
    
    async def create_vacancy(self, vacancy: schemas.VacancyCreate):
        vacancy_model = models.Vacancy(**vacancy.model_dump())
        self.session.add(vacancy_model)
        await self.session.commit()

    async def get_vacancy_files(self) -> List[models.VacancyFile]:
        query = select(self.vacancy_file)
        return await self._all(query=query)

    async def get_vacancy_file_by_id(self, vacancy_file_id: int) -> models.VacancyFile:
        vacancy_file: models.VacancyFile = self.session.get(self.vacancy_file, vacancy_file_id)
        if not vacancy_file:
            logger.warning(f"Vacancy file {vacancy_file_id} is not found")
            raise HTTPException(status_code=404, detail="Not found")
        return vacancy_file
            
    async def create_vacancy_file(self, vacancy_file: schemas.VacancyFileCreate):
        vacancy_file_model = models.VacancyFile(**vacancy_file.model_dump())
        self.session.add(vacancy_file_model)
        await self.session.commit()

    async def get_interviews(self, candidate_id: int, status: str) -> List[models.Interview]:
        query = select(self.interview)
        if candidate_id:
            query = query.where(self.interview.candidate_id == candidate_id)
        if status:
            query = query.where(self.interview.status == status)
        return await self._all(query=query)

    async def get_interview_by_id(self, interview_id: int) -> models.Interview:
        interview: models.Interview = self.session.get(self.interview, interview_id)
        if not interview:
            logger.warning(f"Interview {interview_id} is not found")
            raise HTTPException(status_code=404, detail="Not found")
        return interview
    
    async def create_interview(self, interview: schemas.InterviewCreate):
        interview_model = models.Interview(**interview.model_dump())
        self.session.add(interview_model)
        await self.session.commit()

    async def get_candidates(self) -> List[models.Candidate]:
        query = select(self.candidate)
        return await self._all(query=query)

    async def get_candidate_by_id(self, candidate_id: int) -> models.Candidate:
        candidate: models.Candidate = self.session.get(self.candidate, candidate_id)
        if not candidate:
            logger.warning(f"Candidate {candidate_id} is not found")
            raise HTTPException(status_code=404, detail="Not found")
        return candidate
    
    async def create_candidate(self, candidate: schemas.CandidateCreate):
        candidate_model = models.Candidate(**candidate.model_dump())
        self.session.add(candidate_model)
        await self.session.commit()
