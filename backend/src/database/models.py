from sqlalchemy import (Boolean, Column, Date,
                        ForeignKey, Integer, String,
                        JSON, UUID)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Candidate(Base):
    __tablename__ = "candidate"
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID, unique=True)
    name = Column(String())
    is_referral = Column(Boolean, default=False)
    other_info = Column(JSON)
    resume_link = Column(String())
    status = Column(String())
    vacancy_id = Column(Integer)
    
class Vacancy(Base):
    __tablename__ = "vacancy"
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID, unique=True)
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
    
class VacancyFile(Base):
    __tablename__ = "vacancy_file"
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID, unique=True)
    name = Column(String())
    description = Column(String())
    link = Column(String())
    created_at = Column(Date)
    

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID, unique=True)
    password_hash = Column(String())
    name = Column(String())
    email = Column(String(), unique=True)
    role = Column(String())
    phone = Column(String())
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    
class Interview(Base):
    __tablename__ = "interview"
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID, unique=True)
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
    
    
    
