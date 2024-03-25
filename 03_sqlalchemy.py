from pathlib import Path

import pandas as pd
# func для агрегатных функций SQL, create_engine для подключения к БД
from sqlalchemy import func, create_engine
# sessionmaker для создания сессии
from sqlalchemy.orm import sessionmaker

from custom_libs.models import JobTitle, Company, Vacancy, Salary
from custom_libs.base import Base


# Определение абсолютного пути к корневой директории проекта
project_root_dir = Path(__file__).resolve().parent

# Подключение к базе данных с помощью SQLAlchemy, используя относительный путь
db_path = project_root_dir / 'output_data' / 'job_vacancies.db'
engine = create_engine(f'sqlite:///{db_path}')

# Инициализация подключения к БД SQLite
Session = sessionmaker(bind=engine)


def main() -> None:
    # Создание экземпляра сессии для выполнения операций
    session = Session()

    # Подготовка к записи результатов запросов
    results_dir = Path('sqlalchemy_results')  # Имя директории для сохранения результатов
    # Проверка, существует ли директория
    if not results_dir.exists():
        results_dir.mkdir()    # Если нет, то создаём её

    # Запросы к базе данных и их сохранение в CSV файлы

    # Запрос 1: Количество вакансий в каждой категории.
    query1 = (session.query(JobTitle.category, func.count(Vacancy.id).label('num_vacancies'))
              .join(Vacancy)
              .group_by(JobTitle.category)).statement
    df_query1 = pd.read_sql(query1, engine)
    df_query1.to_csv(results_dir / 'vacancies_per_category.csv', index=False)

    # Запрос 2: Сравнение минимальной и максимальной зарплат в различных секторах.
    query2 = (session.query(
        JobTitle.category,
        func.min(Salary.salary_in_usd).label('min_salary'),
        func.max(Salary.salary_in_usd).label('max_salary')
    ).join(Vacancy, Vacancy.job_title_id == JobTitle.id)
     .join(Salary, Salary.vacancy_id == Vacancy.id)
     .group_by(JobTitle.category)).statement
    df_query2 = pd.read_sql(query2, engine)
    df_query2.to_csv(results_dir / 'salary_range_per_category.csv', index=False)

    # Запрос 3: Средняя зарплата в долларах за каждый год появления вакансии.
    query3 = (session.query(
        JobTitle.work_year,
        func.avg(Salary.salary_in_usd).label('average_salary')
    ).select_from(JobTitle)
     .join(Vacancy, JobTitle.id == Vacancy.job_title_id)
     .join(Salary, Vacancy.id == Salary.vacancy_id)
     .group_by(JobTitle.work_year)).statement
    df_query3 = pd.read_sql(query3, engine)
    df_query3.to_csv(results_dir / 'average_salary_per_year.csv', index=False)

    # Запрос 4: Подсчет количества вакансий по уровню опыта сотрудников.
    query4 = (session.query(
        Vacancy.experience_level,
        func.count(Vacancy.id).label('vacancies_count')
    ).group_by(Vacancy.experience_level)).statement
    df_query4 = pd.read_sql(query4, engine)
    df_query4.to_csv(results_dir / 'vacancies_count_by_experience_level.csv', index=False)

    # Запрос 5: Компании, которые предлагают работу удаленно.
    query5 = (session.query(
        Company.id,
        Company.location,
        Company.size,
        Vacancy.experience_level,
        Vacancy.employment_type,
        Vacancy.work_setting,
        JobTitle.title,
        JobTitle.category,
        Salary.currency,
        Salary.amount,
        Salary.salary_in_usd
    ).select_from(Company)
     .join(Vacancy, Company.id == Vacancy.company_id)
     .join(JobTitle, Vacancy.job_title_id == JobTitle.id)
     .join(Salary, Vacancy.id == Salary.vacancy_id)
     .filter(Vacancy.work_setting == "Remote")).statement
    df_query5 = pd.read_sql(query5, engine)
    df_query5.to_csv(results_dir / 'companies_offering_remote_work.csv', index=False)

    # Закрытие сессии после выполнения всех запросов
    session.close()

    stmt = f'Все запросы успешно выполнены и результаты сохранены в каталоге: {results_dir}'
    print(stmt)


if __name__ == '__main__':
    main()