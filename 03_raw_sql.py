from pathlib import Path

from custom_libs.raw_sql_queries import connect_to_db, create_results_dir, execute_query


# Получаем абсолютный путь к директории скрипта
current_script_dir = Path(__file__).parent.absolute()

# Строим относительный путь к файлу базы данных
db_path = current_script_dir / 'output_data' / 'job_vacancies_raw.db'

# Строим относительный путь к директории для результатов
results_dir = current_script_dir / 'raw_sql_results'


def main() -> None:
    # Устанавливаем соединение и подготавливаем каталог для результатов
    conn = connect_to_db(db_path)
    create_results_dir(results_dir)

    query1 = '''
    -- Запрос 1: Количество вакансий в каждой категории
    SELECT job_titles.category, COUNT(vacancies.id) AS num_vacancies
    FROM job_titles
    JOIN vacancies ON job_titles.id = vacancies.job_title_id
    GROUP BY job_titles.category;
    '''

    query2 = '''
    -- Запрос 2: Подсчет количества вакансий по уровню опыта сотрудников
    SELECT vacancies.experience_level, COUNT(vacancies.id) AS vacancies_count
    FROM vacancies
    GROUP BY vacancies.experience_level;
    '''

    query3 = '''
    -- Запрос 3: Сравнение минимальной и максимальной зарплат в различных секторах
    SELECT job_titles.category, MIN(salaries.salary_in_usd) AS min_salary,
           MAX(salaries.salary_in_usd) AS max_salary
    FROM job_titles
    JOIN vacancies ON vacancies.job_title_id = job_titles.id
    JOIN salaries ON salaries.vacancy_id = vacancies.id
    GROUP BY job_titles.category;
    '''

    query4 = '''
    -- Запрос 4: Компании, которые предлагают работу удаленно
    SELECT companies.id, companies.location, companies.size,
           vacancies.experience_level, vacancies.employment_type,
           vacancies.work_setting, job_titles.title, job_titles.category,
           salaries.currency, salaries.amount, salaries.salary_in_usd
    FROM companies
    JOIN vacancies ON companies.id = vacancies.company_id
    JOIN job_titles ON vacancies.job_title_id = job_titles.id
    JOIN salaries ON vacancies.id = salaries.vacancy_id
    WHERE vacancies.work_setting = 'Remote';
    '''

    query5 = '''
    -- Запрос 5: Средняя зарплата в долларах за каждый год появления вакансии
    SELECT job_titles.work_year, AVG(salaries.salary_in_usd) AS average_salary
    FROM job_titles
    JOIN vacancies ON job_titles.id = vacancies.job_title_id
    JOIN salaries ON vacancies.id = salaries.vacancy_id
    GROUP BY job_titles.work_year;
    '''

    # Выполнение запросов
    try:
        execute_query(query1, 'vacancies_per_category.csv', conn, results_dir)
        execute_query(query2, 'vacancies_count_by_experience_level.csv', conn, results_dir)
        execute_query(query3, 'salary_comparison_by_sector.csv', conn, results_dir)
        execute_query(query4, 'remote_job_offers.csv', conn, results_dir)
        execute_query(query5, 'average_salary_by_work_year.csv', conn, results_dir)

        # Сообщаем о успешном выполнении запросов и сохранении результатов
        print(f"Все запросы успешно выполнены и результаты сохранены в каталоге: {results_dir}")

    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
    finally:
        # Закрытие соединения с базой данных
        conn.close()


if __name__ == "__main__":
    main()