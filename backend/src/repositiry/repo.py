from src.database import models
from src.schema import schemas


class Repository:
    user = models.User
    vacancy = models.Vacancy
    vacancy_file = models.VacancyFile
    interview = models.Interview
    candidate = models.Candidate

    def __init__(self, session):
        self.session = session
        
    async def create_user(self, user: schemas.UserCreate):
        user_model = models.User(**user.model_dump())
        self.session.add(user_model)
        await self.session.commit()
    
    async def create_vacancy(self, vacancy: schemas.VacancyCreate):
        vacancy_model = models.Vacancy(**vacancy.model_dump())
        self.session.add(vacancy_model)
        await self.session.commit()
            
    async def create_vacancy_file(self, vacancy_file: schemas.VacancyFileCreate):
        vacancy_file_model = models.VacancyFile(**vacancy_file.model_dump())
        self.session.add(vacancy_file_model)
        await self.session.commit()
    
    async def create_interview(self, interview: schemas.InterviewCreate):
        interview_model = models.Interview(**interview.model_dump())
        self.session.add(interview_model)
        await self.session.commit()
    
    async def create_candidate(self, candidate: schemas.CandidateCreate):
        candidate_model = models.Candidate(**candidate.model_dump())
        self.session.add(candidate_model)
        await self.session.commit()
