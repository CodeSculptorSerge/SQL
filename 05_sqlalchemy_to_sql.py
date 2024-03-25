from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


# Определяем абсолютное местоположение скрипта
project_root_dir = Path(__file__).resolve().parent

# Формируем абсолютный путь к файлу базы данных
db_path = project_root_dir / 'output_data' / 'job_vacancies.db'

# Создаём движок SQLAlchemy с использованием относительного пути
engine = create_engine(f'sqlite:///{db_path}')


def main() -> None:
    # Подключаемся и изучаем данные
    df = pd.read_sql_table('job_titles', engine)
    # df.head()
    # df.shape
    # category_counts = df['category'].value_counts()
    # df.info()

    # Переименовываем столбец work_year
    # df['work_year'].unique()
    df = df.rename(columns={'work_year': 'year'})
    # df.columns

    # Обновляем название вакансий, содержащих "Data Engineer" в названии
    df['title'] = df['title'].replace(to_replace=r'.*Data Engineer.*', value='My Future Job', regex=True)

    # Удаляем вакансии, содержащие в названии "BI"
    # Извлекаем и исключаем названия с "BI"
    df = df[~df['title'].str.contains(r'\bBI\b', na=False, regex=True)]

    # Заменяем исходную таблицу в базе данных на обновленную версию без индекса
    df.to_sql('JobTitles', con=engine, if_exists='replace', index=False)


if __name__ == '__main__':
    main()