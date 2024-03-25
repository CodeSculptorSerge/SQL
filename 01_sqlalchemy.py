from pathlib import Path

# create_engine позволяет указать конфигурацию базы данных, например тип базы данных, имя и т.д.
from sqlalchemy import create_engine, inspect, Column, Integer, String, Float, ForeignKey
# declarative_base используется для объявления моделей, представляющих таблицы в базе данных.
# relationship используется для определения связи между моделями (подобно внешним ключам).
# sessionmaker является фабрикой для производства новых объектов Session при вызове.
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from custom_libs.models import JobTitle, Company, Vacancy, Salary
from custom_libs.base import Base


# Получаем абсолютный путь к директории, в которой находится скрипт.
current_script_dir = Path(__file__).resolve().parent

# Строим абсолютный путь к файлу базы данных относительно директории скрипта.
db_path = current_script_dir / 'output_data' / 'job_vacancies.db'


def main() -> None:
    # Создаем движок SQLite, который определяет имя и расположение нашей базы данных.
    engine = create_engine(f'sqlite:///{db_path}')

    # Создаем все таблицы, определенные подклассами Base (нашими моделями), если они еще не существуют в базе данных.
    Base.metadata.create_all(bind=engine)

    # Создаем объект sessionmaker, связанный с нашим движком.
    # С помощью sessionmaker мы можем создавать объекты Session,
    # которые управляют операциями по сохранению для объектов, отображаемых через ORM.
    Session = sessionmaker(bind=engine)

    # Инициализируем объект Session, который служит интерфейсом для взаимодействия с базой данных.
    # Через сессию мы можем выполнять запросы к базе данных и манипулировать данными.
    session = Session()

    print("База данных и таблицы успешно созданы через SQLAlchemy.")

    inspector = inspect(engine)
    print(inspector.get_table_names())


if __name__ == "__main__":
    main()