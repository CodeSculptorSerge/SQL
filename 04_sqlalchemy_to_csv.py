from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, inspect


# Определяем абсолютный путь к директории скрипта
project_root_dir = Path(__file__).resolve().parent

# Формируем путь к файлу базы данных, используя относительный путь
db_path = project_root_dir / 'output_data' / 'job_vacancies.db'
engine = create_engine(f'sqlite:///{db_path}')


def main() -> None:
    # Настройка инспектора для получения информации о таблицах в базе данных
    inspector = inspect(engine)
    # Получение списка всех названий таблиц в базе данных
    tables = inspector.get_table_names()

    # Вывод структуры и содержимого таблиц для последующего анализа
    for table_name in tables:
        df = pd.read_sql_table(table_name, engine)
        # print(f"Таблица: {table_name}")
        # print(df.head())
        # print("\n")

    # Выборка, фильтрация и интеграция специфических данных для дальнейшего анализа

    # Загружаем данные из таблицы 'job_titles' и фильтруем по категории и году
    job_titles_df = pd.read_sql_table('job_titles', engine)

    job_titles_filtered = job_titles_df[
        (job_titles_df['category'] == 'Data Engineering') &
        (job_titles_df['work_year'] == 2023)
    ]

    # Загружаем только нужные столбцы данных из таблицы 'salaries'
    salaries_df = pd.read_sql_table('salaries', engine)
    salaries_filtered = salaries_df[['id', 'salary_in_usd']]

    # Загружаем и фильтруем столбцы из таблицы 'vacancies'
    vacancies_df = pd.read_sql_table('vacancies', engine)
    experience_filtered = vacancies_df[['id', 'experience_level']]

    # Объединение отфильтрованных DataFrame'ов
    merged_df = pd.merge(pd.merge(job_titles_filtered, salaries_filtered, on='id'), experience_filtered, on='id')

    # Формируем абсолютный путь к файлу, куда будет сохранен CSV
    csv_file_path = project_root_dir / 'output_data' / 'sqlalchemy_to_csv.csv'

    # Сохраняем DataFrame в CSV без индекса
    merged_df.to_csv(csv_file_path, index=False)

    # Выводим подтверждение о том, что все запросы успешно выполнены и результаты сохранены
    stmt = f'CSV файл успешно сохранён в каталоге: {csv_file_path}'
    print(stmt)


if __name__ == '__main__':
    main()