from src.database import models
from src.schema import schemas
from src.settings import logger
from fastapi import HTTPException
from sqlalchemy import select
from typing import List


class RepositoryBase:
    """ Базовый класс обращения в БД """
    def __init__(self, session):
        self.session = session

    async def _all(self, query):
        query_result = await self.session.execute(query)
        rows = query_result.all()
        return [data[0] for data in rows if data[0]]

    @staticmethod
    async def _first(result):
        result = result.first()
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

    async def get_users(self) -> List[models.User]:
        query = select(self.user)
        return await self._all(query=query)

    async def create_user(self, user: schemas.UserCreate):
        user_model = models.User(**user.model_dump())
        self.session.add(user_model)
        await self.session.commit()

    async def get_vacancies(self) -> List[models.Vacancy]:
        query = select(self.vacancy)
        return await self._all(query=query)
    
    async def create_vacancy(self, vacancy: schemas.VacancyCreate):
        vacancy_model = models.Vacancy(**vacancy.model_dump())
        self.session.add(vacancy_model)
        await self.session.commit()

    async def get_vacancy_files(self) -> List[models.VacancyFile]:
        query = select(self.vacancy_file)
        return await self._all(query=query)
            
    async def create_vacancy_file(self, vacancy_file: schemas.VacancyFileCreate):
        vacancy_file_model = models.VacancyFile(**vacancy_file.model_dump())
        self.session.add(vacancy_file_model)
        await self.session.commit()

    async def get_interviews(self) -> List[models.Interview]:
        query = select(self.interview)
        return await self._all(query=query)
    
    async def create_interview(self, interview: schemas.InterviewCreate):
        interview_model = models.Interview(**interview.model_dump())
        self.session.add(interview_model)
        await self.session.commit()

    async def get_candidates(self, vacancy_id: int) -> List[models.Candidate]:
        query = select(self.candidate)
        if vacancy_id:
            query = query.where(self.candidate.vacancy_id == vacancy_id)
        return await self._all(query=query)
    
    async def create_candidate(self, candidate: schemas.CandidateCreate):
        candidate_model = models.Candidate(**candidate.model_dump())
        self.session.add(candidate_model)
        await self.session.commit()
