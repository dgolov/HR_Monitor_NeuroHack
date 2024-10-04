

from pydantic import BaseModel


class User(BaseModel):
    name: str
    

class Vacancy(BaseModel):
    title: str
    
class VacancyFile(BaseModel):
    name: str

class Interview(BaseModel):
    title: str
    

class Candidate(BaseModel):
    name: str