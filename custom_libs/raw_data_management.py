import pandas as pd
import sqlite3


def read_csv(file_path):
    """
    Читаем данные из CSV файла.
    Возвращаем DataFrame с прочитанными данными.
    """
    return pd.read_csv(file_path)

def connect_to_db(db_path):
    """
    Подключаемся к базе данных SQLite по указанному пути.
    Возвращаем объект соединения.
    """
    return sqlite3.connect(db_path)

def prepare_data_for_insert(df):
    """
    Подготавливаем данные для вставки в базу данных из DataFrame.
    Возвращаем кортежи с данными для каждой таблицы.
    """
    job_titles_data = [(row['job_title'], row['job_category'], row['work_year']) for index, row in df.iterrows()]
    companies_data = [(row['company_location'], row['company_size']) for index, row in df.iterrows()]
    vacancies_data = [(index+1, index+1, row['employee_residence'], row['experience_level'], row['employment_type'], row['work_setting']) for index, row in df.iterrows()]
    salaries_data = [(index+1, row['salary_currency'], row['salary'], row['salary_in_usd']) for index, row in df.iterrows()]
    return job_titles_data, companies_data, vacancies_data, salaries_data

def insert_into_table(cursor, table, columns, values_list):
    """
    Вставляем данные в таблицу.
    Выполняем массовую вставку данных values_list в указанную таблицу table.
    """
    placeholders = ', '.join('?' * len(columns))
    columns_formatted = ', '.join(columns)
    cursor.executemany(f"INSERT INTO {table} ({columns_formatted}) VALUES ({placeholders})", values_list)
