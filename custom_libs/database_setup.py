from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base


def init_db():
    # Получаем абсолютный путь к корневой директории проекта
    project_root_dir = Path(__file__).resolve().parent.parent

    # Строим абсолютный путь к файлу базы данных, относительно директории скрипта
    db_path = project_root_dir / 'output_data' / 'job_vacancies.db'

    # Создаем движок SQLite, который определяет имя и расположение нашей базы данных
    engine = create_engine(f'sqlite:///{db_path}')

    # Создаем структуру БД, если её нет
    Base.metadata.create_all(bind=engine)

    # Создаем класс сессии
    Session = sessionmaker(bind=engine)

    return Session()
