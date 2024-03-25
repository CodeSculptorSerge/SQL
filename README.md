# Руководство по работе с базой данных вакансий

Это руководство описывает процедуры, которые помогут вам эффективно взаимодействовать с базой данных вакансий. В нём рассмотрены моменты подготовки базы данных (БД), загрузки данных в неё, выполнение запросов для анализа информации, экспорт результатов и обновление данных для поддержания их актуальности.

## Создание Базы Данных

`01_sqlalchemy.py`
- Создание и настройка БД с использованием SQLAlchemy ORM.
- Процесс включает: подключение с create_engine, описание таблиц с declarative_base, инициализация таблиц с Base.metadata.create_all, создание сессии Session.

`01_raw_sql.py`
- Создание БД с использованием чистого SQL.
- Процесс: подключение через sqlite3, создание таблиц с уникальными ключами и внешними связями, выполнение скриптов SQL, закрытие соединения.
- Результат: получена БД job_vacancies_raw.db с необходимыми таблицами.

## Вставка Данных в БД

`02_sqlalchemy.py`
- Вставка данных из файла CSV в БД с помощью SQLAlchemy.
- Этапы: чтение файла CSV (через Pandas), создание объектов данных, сбор их в список и добавление в БД с помощью session.add_all(), сохранение изменений session.commit().
- Для избежания ошибок используется блок обработки исключений try-except для возможного отката session.rollback.

`02_raw_sql.py`
- Вставка данных сразу большими партиями через sqlite3 и Pandas.
- Этапы: чтение CSV, подготовка данных, вставка с cursor.executemany(), использование try-except-finally для контроля ошибок.
- Данные успешно добавлены в job_vacancies_raw.db.

## Выполнение Запросов

> [!info] Индексы в Базе Данных
При проектировании схемы таблиц базы данных я определил только первичные ключи, что позволило обеспечить быстрый доступ к уникальным записям. Однако для столбцов, используемых в фильтрации и сортировке, я не установил дополнительные индексы (index=true). Это означает, что, хотя выполнение запросов с фильтрацией становится менее эффективным из-за необходимости полного сканирования таблиц, скорость вставки новых данных увеличивается, поскольку отсутствие индексов устраняет накладные расходы на их обновление при каждом добавлении записи. В результате получилось ускорить процесс добавления данных за счёт замедления выполнения запросов, которые могут требовать более длительного времени из-за сложности их выполнения без поддержки индексов.

`03_sqlalchemy.py`
- Выполнение запросов и сохранение их в CSV средствами SQLAlchemy.
- Процедура: подключение к БД, создание папки для файлов, составление и выполнение запросов с использованием ORM, запись результатов в CSV файлы.

Выполнены запросы, такие как:
  - Подсчёт количества вакансий по категориям.
  - Оценка вакансий в зависимости от опыта кандидатов.
  - Сравнение зарплатных предложений в различных секторах.
  - Поиск компаний, предоставляющих возможность удалённой работы.
  - Расчёт средних зарплат в долларах по годам выкладывания вакансий.

`03_raw_sql.py`
- Выполнение запросов SQL и запись результатов в CSV.
- Процесс: соединение с SQLite через sqlite3, создание папки, выполнение запросов с функцией execute_query() и сохранение результатов в CSV.
- Данные получены по запросам о работе, опыте, зарплатах, удалённой работе и средней заработной плате по годам.

## Анализ и Экспорт Данных

`04_sqlalchemy_to_csv.ipynb`
- Подключение к БД через SQLAlchemy.
- Анализ данных, их фильтрация и объединение с помощью Pandas DataFrame.
- Запись отфильтрованной информации в файл CSV.

## Обновление и Очистка Данных

`05_sqlalchemy_to_sql.ipynb`
- Экспорт данных из Pandas DataFrame в CSV с помощью метода DataFrame.to_csv().
- Обновление и удаление данных осуществляется через сессии SQLAlchemy.

