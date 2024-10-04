from datetime import datetime

import uuid
from pydantic import BaseModel
from pydantic.v1 import UUID4


class User(BaseModel):
    uuid: str
    name: str
    email: str
    role: str
    phone: str
    is_verified: bool
    is_active: bool


class UserCreate(BaseModel):
    name: str
    password_hash: str
    email: str
    role: str
    phone: str
    is_verified: bool
    is_active: bool


class Vacancy(BaseModel):
    uuid: str
    description: str
    status: str
    created_at: datetime
    open_at: datetime
    updated_at: datetime
    close_at: datetime
    viewed_count: int
    responded_count: int
    vacancy_file_id: int
    creator_id: int


class VacancyCreate(BaseModel):
    uuid: UUID4 = uuid.uuid4()
    description: str
    status: str = 'blank'
    created_at: datetime = datetime.now()
    open_at: datetime | None = None
    updated_at: datetime | None = None
    close_at: datetime | None = None
    viewed_count: int = 0
    responded_count: int = 0
    vacancy_file_id: int  | None = None
    creator_id: int


class VacancyFile(BaseModel):
    uuid: UUID4 = uuid.uuid4()
    name: str
    description: str
    link: str
    created_at: datetime

class VacancyFileCreate(BaseModel):
    uuid: UUID4 = uuid.uuid4()
    name: str
    description: str
    link: str
    created_at: datetime = datetime.now()

class Interview(BaseModel):
    id : int
    uuid : UUID4
    title : str
    description : str
    candidate_id : int
    type : str
    recruiter_id : int
    tech_id : int
    status : str
    other_info : str
    created_at : datetime
    date_start_at : datetime
    date_end_at : datetime


class InterviewCreate(BaseModel):
    uuid : UUID4 = uuid.uuid4()
    title : str
    description : str
    candidate_id : int
    type : str
    recruiter_id : int
    tech_id : int
    status : str
    other_info : str
    created_at : datetime = datetime.now()
    date_start_at : datetime | None = None
    date_end_at : datetime | None = None


class Candidate(BaseModel):
    id: int
    uuid: UUID4
    name: str
    is_referral: bool
    other_info: str
    resume_link: str
    status: str
    vacancy_id: int


class CandidateCreate(BaseModel):
    id: int
    uuid: UUID4 = uuid.uuid4()
    name: str
    is_referral: bool = False
    other_info: str
    resume_link: str
    status: str
    vacancy_id: int
