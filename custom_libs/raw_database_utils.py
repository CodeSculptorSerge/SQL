import sqlite3


def create_connection(db_path):
    """Создает подключение к SQLite базе данных по указанному пути."""
    conn = sqlite3.connect(db_path)
    return conn

def create_tables(conn):
    """Создаем таблицы в базе данных."""
    sql_commands = """
    CREATE TABLE IF NOT EXISTS job_titles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        category TEXT,
        work_year INTEGER
    );

    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT,
        size TEXT
    );

    CREATE TABLE IF NOT EXISTS vacancies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title_id INTEGER NOT NULL,
        company_id INTEGER NOT NULL,
        residence TEXT,
        experience_level TEXT,
        employment_type TEXT,
        work_setting TEXT,
        FOREIGN KEY (job_title_id) REFERENCES job_titles(id),
        FOREIGN KEY (company_id) REFERENCES companies(id)
    );

    CREATE TABLE IF NOT EXISTS salaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vacancy_id INTEGER NOT NULL,
        currency TEXT,
        amount REAL,
        salary_in_usd REAL,
        FOREIGN KEY (vacancy_id) REFERENCES vacancies(id)
    );
    """
    cursor = conn.cursor()
    cursor.executescript(sql_commands)
    conn.commit()

def list_tables(conn):
    """Выводим список всех таблиц в базе данных."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Список созданных таблиц:")
    for table in tables:
        print(table[0])
