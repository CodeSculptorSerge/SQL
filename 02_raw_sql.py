from pathlib import Path

import sqlite3

from custom_libs.raw_data_management import insert_into_table, read_csv, connect_to_db, prepare_data_for_insert


# Получаем абсолютный путь к директории скрипта
current_script_dir = Path(__file__).parent.absolute()

# Строим относительный путь к файлу CSV
csv_file_path = current_script_dir / 'input_data' / 'jobs_in_data.csv'

# Строим относительный путь к файлу базы данных
db_path = current_script_dir / 'output_data' / 'job_vacancies_raw.db'


def main() -> None:
    try:
        # Читаем данные из CSV и подключаемся к базе данных
        df = read_csv(csv_file_path)
        conn = connect_to_db(db_path)
        cursor = conn.cursor()

        # Подготавливаем данные для вставки
        job_titles_data, companies_data, vacancies_data, salaries_data = prepare_data_for_insert(df)

        # Вставляем данные в соответствующие таблицы
        insert_into_table(cursor, 'job_titles', ['title', 'category', 'work_year'], job_titles_data)
        insert_into_table(cursor, 'companies', ['location', 'size'], companies_data)
        insert_into_table(cursor, 'vacancies', ['job_title_id', 'company_id', 'residence', 'experience_level', 'employment_type', 'work_setting'], vacancies_data)
        insert_into_table(cursor, 'salaries', ['vacancy_id', 'currency', 'amount', 'salary_in_usd'], salaries_data)

        conn.commit()

    except sqlite3.IntegrityError as e:
        print(f"Ошибка целостности данных: {e}")
        conn.rollback()  # Откат изменений при наличии ошибки

    except sqlite3.DatabaseError as e:
        print(f"Ошибка базы данных: {e}")
        conn.rollback()  # Откат изменений при наличии ошибки

    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        conn.rollback()  # Откат изменений при наличии ошибки

    finally:
        # Закрываем соединение с базой данных
        cursor.close()
        conn.close()
        print("Процесс добавления данных завершён.")


if __name__ == "__main__":
    main()