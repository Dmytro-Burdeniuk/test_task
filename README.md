# Credit Planner API

📌 **Проект для управління кредитами та планами виконання**  
Використовує FastAPI, SQLAlchemy та базу даних PostgreSQL/MySQL/SQLite. Підтримує імпорт планів з Excel, звіти по виконанню планів та інформацію по користувачам.

---

## Основні можливості

1. Імпорт планів з Excel.
2. Перегляд виконання планів на конкретну дату.
3. Річний звіт по місяцях з підрахунком виконання планів.
4. Інформація про кредити конкретного користувача.

---

## Структура проекту

```text
src/
│
├─ database.py # Налаштування SQLAlchemy та підключення до БД
├─ models.py # ORM моделі
├─ schemas/ # Схеми Pydantic для валідації
│ ├─ schemas_base.py 
│ ├─ schemas_logic.py
├─ crud.py # Функції для роботи з БД (Insert, Select, Aggregation)
├─ routes/
│ ├─ plans.py # Endpoints для імпорту та роботи з планами
│ ├─ reports.py # Endpoints для звітів
│ └─ users.py # Endpoints для користувачів
└─ main.py # FastAPI додаток та запуск сервера
```

## Установка

1. Клонування репозиторію:

```bash
git clone <https://github.com/Dmytro-Burdeniuk/test_task>
cd <test_taskr>
```

2. Віртуальне середовище:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Встановлення залежностей:

```bash
pip install -r requirements.txt
```

4. Створення .env файлу з підключенням до БД:

```python
DB_URL=mysql+pymysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```

5. Створення таблиць та запуск сервера:

```bash
python src/main.py
# або
uvicorn src.main:app --reload
```


Технології:
- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL/MySQL/SQLite
- Pandas (для імпорту Excel)
- Pydantic
- Uvicorn (ASGI сервер)