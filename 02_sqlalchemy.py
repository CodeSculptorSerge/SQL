from pathlib import Path

from custom_libs.database_setup import init_db
from custom_libs.data_loader import load_data


# Определение абсолютного пути к корневой директории проекта
project_root_dir = Path(__file__).resolve().parent
    
# Строим абсолютный путь к CSV файлу, относительно корневой директории проекта
csv_file_path = project_root_dir / 'input_data' / 'jobs_in_data.csv'


def main() -> None:
    session = init_db()
    
    load_data(session, csv_file_path)


if __name__ == '__main__':
    main()
