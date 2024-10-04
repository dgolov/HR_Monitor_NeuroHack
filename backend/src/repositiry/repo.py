from src.database import models
from src.schema import schemas

class Repository:
    user = models.User
    vacancy = models.Vacancy
    vacancy_file = models.VacancyFile
    interview = models.Interview
    candidate = models.Candidate
    def __init__(self, session_factory):
        self.session = session_factory()
        
    async def create_user(self, user: schemas.User):
        user_model = models.User(**user.model_dump())
        self.session.add(user_model)
        await self.session.commit()
    
    async def create_vacancy(self, vacancy: schemas.Vacancy):
        vacancy_model = models.Vacancy(**vacancy.model_dump())
        self.session.add(vacancy_model)
        await self.session.commit()
            
    async def create_vacancy_file(self, vacancy_file: schemas.VacancyFile):
        vacancy_file_model = models.VacancyFile(**vacancy_file.model_dump())
        self.session.add(vacancy_file_model)
        await self.session.commit()
            
    
    async def create_interview(self, interview: schemas.Interview):
        interview_model = models.Interview(**interview.model_dump())
        self.session.add(interview_model)
        await self.session.commit()
    
    async def create_candidate(self, candidate: schemas.Candidate):
        candidate_model = models.Candidate(**candidate.model_dump())
        self.session.add(candidate_model)
        await self.session.commit()