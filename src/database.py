import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from contextlib import contextmanager


load_dotenv()

URL_DATABASE = os.getenv("DB_URL")

# Створюємо SQLAlchemy engine для підключення до бази даних
engine = create_engine(URL_DATABASE, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


# Базовий клас для моделей SQLAlchemy
class Base(DeclarativeBase):
    """
    Базовий клас для оголошення моделей.
    Усі моделі повинні наслідувати цей клас.
    """

    pass


def get_db():
    """
    Генератор сесії бази даних для FastAPI Depends.

    Використання:
    ```python
    def endpoint(db: Session = Depends(get_db)):
        ...
    ```

    Логіка:
    - Створює сесію
    - Повертає її для використання в endpoint
    - Закриває сесію після завершення роботи endpoint
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
