

from pydantic import BaseModel


class User(BaseModel):
    uuid: str
    name: str
    email: str
    role: str
    phone: str
    is_verified: bool
    is_active: bool


class CreateUser(BaseModel):
    name: str
    password_hash: str
    email: str
    role: str
    phone: str
    is_verified: bool
    is_active: bool


class Vacancy(BaseModel):
    title: str
    title: str
    title: str
    title: str
    title: str
    title: str

class VacancyFile(BaseModel):
    name: str
    name: str
    name: str
    name: str

class Interview(BaseModel):
    title: str
    title: str
    title: str
    title: str
    title: str


class Candidate(BaseModel):
    name: str
    name: str
    name: str
    name: str
    name: str
    name: str