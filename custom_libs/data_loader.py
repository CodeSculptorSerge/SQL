import pandas as pd
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .models import JobTitle, Company, Vacancy, Salary


def load_data(session, csv_file_path):
    df = pd.read_csv(csv_file_path)

    try:
        objects_to_add = []  # Создаем список для хранения объектов
  
        for index, row in df.iterrows():
            job_title = JobTitle(
                title=row['job_title'],
                category=row['job_category'],
                work_year=row['work_year']
            )

            company = Company(
                location=row['company_location'],
                size=row['company_size']
            )

            vacancy = Vacancy(
                job_title=job_title,
                company=company,
                residence=row['employee_residence'],
                experience_level=row['experience_level'],
                employment_type=row['employment_type'],
                work_setting=row['work_setting']
            )

            salary = Salary(
                vacancy=vacancy,
                currency=row['salary_currency'],
                amount=row['salary'],
                salary_in_usd=row['salary_in_usd']
            )

            objects_to_add.extend([job_title, company, vacancy, salary])

        session.add_all(objects_to_add)

        session.flush()
        session.commit()
        print('Данные успешно добавлены.')
    except IntegrityError as e:
        session.rollback()
        print(f"Ошибка целостности данных в базе: {e}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Ошибка добавления данных в базу: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
