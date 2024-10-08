import uuid
from datetime import date, datetime
from typing import Dict, Optional

from pydantic import UUID4, BaseModel, ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class User(Base):
    uuid: UUID4
    id: int
    name: str
    email: str
    role: str
    phone: str
    is_verified: bool
    is_active: bool
    grade: int | None = None
    efficiently: int | None = None

    class Config:
        from_attributes = True


class UserCreate(Base):
    name: str
    password_hash: str
    email: str
    role: str
    phone: str
    is_verified: bool
    is_active: bool


class Vacancy(Base):
    uuid: UUID4
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

    recruiter: Optional[User]

    class Config:
        from_attributes = True


class VacancyCreate(Base):
    uuid: UUID4 = uuid.uuid4()
    description: str
    status: str = "blank"
    created_at: datetime = datetime.now()
    open_at: datetime | None = None
    updated_at: datetime | None = None
    close_at: datetime | None = None
    viewed_count: int = 0
    responded_count: int = 0
    vacancy_file_id: int | None = None
    creator_id: int


class VacancyFile(Base):
    uuid: UUID4 = uuid.uuid4()
    name: str
    description: str
    link: str
    created_at: datetime


class VacancyFileCreate(Base):
    name: str
    description: str
    link: str
    created_at: datetime = datetime.now()


class Interview(Base):
    id: int
    uuid: UUID4
    title: str
    description: str
    candidate_id: int
    type: str
    recruiter_id: int
    tech_id: int
    status: str
    other_info: str
    created_at: datetime
    date_start_at: datetime
    date_end_at: datetime


class InterviewCreate(Base):
    description: str
    candidate_id: int
    type: str
    recruiter_id: int
    tech_id: int
    status: str
    other_info: str
    created_at: datetime = datetime.now()
    date_start_at: datetime | None = None
    date_end_at: datetime | None = None


class Candidate(Base):
    id: int
    uuid: UUID4
    name: str
    is_referral: bool
    other_info: dict
    resume_link: str
    status: str
    vacancy_id: int


class CandidateCreate(Base):
    name: str
    is_referral: bool = False
    other_info: dict
    resume_link: str
    status: str
    vacancy_id: int


class MonthData(BaseModel):
    average_closure_time_in_days: float
    vacancies_count: int


class VacancyAverageTimeResponse(BaseModel):
    data: Dict[int, Dict[int, MonthData]]


class Metrics(BaseModel):
    id: int
    recruiter_name: str
    month: date
    value: float


class ScreenTimeMetrics(Metrics): ...


class HireTimeMetrics(Metrics): ...


class HireQualityMetrics(Metrics): ...


class OwnerSatisfaction(Metrics): ...


class VacancyCostMetrics(Metrics): ...


class VacancyCostMetricsComparison(Metrics):
    is_referral: bool


class ReferralCountResponse(BaseModel):
    total_hired: int
    referral_count: int
    non_referral_count: int


class HiredRejectedResponse(BaseModel):
    total_count: int
    hired_count: int
    rejected_count: int


class Hired2Fired(BaseModel):
    hired_count: int
    fired_count: int


class EmployeeCountResponse(BaseModel):
    total_fired_less_than_6_months: int


class RecruiterTask(BaseModel):
    uuid: UUID4 = uuid.uuid4()
    type: str
    recruiter_id: int
    description: str
    status: str
    priority: int
    created_at: datetime
    started_at: datetime
    closed_at: datetime
    recruiter: Optional[User]

    class Config:
        from_attributes = True


class MonthRating(BaseModel):
    average_satisfaction_level: float


class RecruiterMonthlyRatings(BaseModel):
    month_data: Dict[int, MonthRating]


class RecruiterRatingsResponse(BaseModel):
    recruiter_data: Dict[str, RecruiterMonthlyRatings]


class VacanciesMonthData(BaseModel):
    vacancies_count: int
    vacancy_cost: float


class VacanciesYearData(BaseModel):
    months: Dict[int, VacanciesMonthData]  # ключ — это номер месяца


class VacancyCostResponse(BaseModel):
    years: Dict[int, VacanciesYearData]  # ключ — это год
