from uuid import uuid4

from sqlalchemy import JSON, UUID, Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Candidate(Base):
    __tablename__ = "candidate"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, unique=True, default=uuid4)
    name = Column(String())
    is_referral = Column(Boolean, default=False)
    other_info = Column(JSON)
    resume_link = Column(String())
    status = Column(String())
    vacancy_id = Column(Integer, ForeignKey("vacancy.id"))


class Vacancy(Base):
    __tablename__ = "vacancy"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, unique=True, default=uuid4)
    title = Column(String())
    description = Column(String())
    status = Column(String())
    created_at = Column(Date)
    open_at = Column(Date)
    updated_at = Column(Date)
    close_at = Column(Date)
    viewed_count = Column(Integer, default=0)
    responded_count = Column(Integer, default=0)
    vacancy_file_id = Column(Integer)
    creator_id = Column(Integer)
    recruiter_id = Column(Integer, ForeignKey("user.id"))
    closing_cost = Column(Integer, default=0)
    is_referral = Column(Boolean, default=False)

    recruiter = relationship("User")


class VacancyFile(Base):
    __tablename__ = "vacancy_file"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, unique=True, default=uuid4)
    name = Column(String())
    description = Column(String())
    link = Column(String())
    created_at = Column(Date)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, unique=True, default=uuid4)
    password_hash = Column(String())
    name = Column(String(), unique=True)
    email = Column(String(), unique=True)
    role = Column(String())
    phone = Column(String())
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    salary = Column(Integer)
    grade = Column(Integer)
    efficiently = Column(Integer)

    employees = relationship("Employee", back_populates="recruiter")


class RecruiterTask(Base):
    __tablename__ = "recruiter_task"
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID, unique=True)
    type = Column(String())
    recruiter_id = Column(Integer, ForeignKey("user.id"))
    description = Column(String())
    status = Column(String())
    priority = Column(Integer)
    created_at = Column(Date)
    started_at = Column(Date)
    closed_at = Column(Date)

    recruiter = relationship("User")


class Interview(Base):
    __tablename__ = "interview"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, unique=True, default=uuid4)
    title = Column(String())
    description = Column(String())
    candidate_id = Column(Integer, ForeignKey("candidate.id"))
    type = Column(String())
    recruiter_id = Column(Integer, ForeignKey("user.id"))
    tech_id = Column(Integer, ForeignKey("user.id"))
    status = Column(String())
    other_info = Column(JSON)
    created_at = Column(Date)
    date_start_at = Column(Date)
    date_end_at = Column(Date)


class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String())
    date_started = Column(Date)
    date_fired = Column(Date)
    position = Column(String)
    cost_of_hiring = Column(Integer)
    manager_rating = Column(Integer)
    recruiter_id = Column(Integer, ForeignKey("user.id"))

    recruiter = relationship("User", back_populates="employees")


class ScreenTimeMetrics(Base):
    __tablename__ = "screen_time_metrics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    recruiter_name = Column(String())
    month = Column(Date)
    value = Column(Float)


class Metrics(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    recruiter_name = Column(String())
    month = Column(Date)
    value = Column(Float)


class HireQualityMetrics(Metrics):
    __tablename__ = "hire_quality_metrics"


class HireTimeMetrics(Metrics):
    __tablename__ = "hire_time_metrics"


class OwnerSatisfactionMetrics(Metrics):
    __tablename__ = "owner_satisfaction_metrics"


class AverageCandidateToVacancyMetrics(Metrics):
    __tablename__ = "average_candidate_to_vacancy_metrics"


class VacancyCostMetrics(Metrics):
    __tablename__ = "vacancy_cost_metrics"


class VacancyCostComparisonMetrics(Metrics):
    __tablename__ = "vacancy_cost_comparison_metrics"
    is_referral = Column(Boolean, default=False)
