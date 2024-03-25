from pathlib import Path

import pandas as pd
import sqlite3



def connect_to_db(db_path):
    """Устанавливаем соединение с SQLite базой данных."""
    conn = sqlite3.connect(db_path)
    return conn

def create_results_dir(results_dir):
    """Создаем директорию для результатов, если она не существует."""
    Path(results_dir).mkdir(parents=True, exist_ok=True)

def execute_query(query, filename, conn, results_dir):
    """Выполнение SQL-запроса с сохранением результатов в CSV файл."""
    df = pd.read_sql_query(query, conn)
    (Path(results_dir) / filename).write_text(df.to_csv(index=False))
