from pathlib import Path

from custom_libs.raw_database_utils import create_connection, create_tables, list_tables


# Получаем абсолютный путь к директории скрипта
current_script_dir = Path(__file__).resolve().parent
    
# Строим относительный путь к файлу базы данных
db_path = current_script_dir / 'output_data' / 'job_vacancies_raw.db'


def main() -> None:
    # Создаём подключение к базе данных
    conn = create_connection(db_path)
    
    # Создаём таблицы в базе данных
    create_tables(conn)

    # Выводим список всех таблиц в базе данных
    list_tables(conn)

    # Закрываем соединение с базой данных
    conn.close()


if __name__ == "__main__":
    main()
