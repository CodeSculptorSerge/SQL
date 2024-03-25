from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

from .base import Base


class JobTitle(Base):
    __tablename__ = 'job_titles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    category = Column(String)
    work_year = Column(Integer)
    # Указываем, что 'job_title' в Vacancy ссылается сюда
    vacancies = relationship("Vacancy", back_populates="job_title")

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    location = Column(String)
    size = Column(String)
    # следует добавить relationship, если хотите двустороннюю связь с Vacancy
    vacancies = relationship("Vacancy", back_populates="company")

class Vacancy(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True)
    job_title_id = Column(Integer, ForeignKey('job_titles.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    residence = Column(String)
    experience_level = Column(String)
    employment_type = Column(String)
    work_setting = Column(String)
    # Устанавливаем двустороннюю связь с JobTitle
    job_title = relationship("JobTitle", back_populates="vacancies")
    # Устанавливаем двустороннюю связь с Company
    company = relationship("Company", back_populates="vacancies")
    # Для Salary тоже указываем обратную связь
    salary = relationship("Salary", uselist=False, back_populates="vacancy")

class Salary(Base):
    __tablename__ = 'salaries'
    id = Column(Integer, primary_key=True)
    vacancy_id = Column(Integer, ForeignKey('vacancies.id'))
    currency = Column(String)
    amount = Column(Float)
    salary_in_usd = Column(Float)
    # Указываем на обратную связь с Vacancy
    vacancy = relationship("Vacancy", back_populates="salary")
