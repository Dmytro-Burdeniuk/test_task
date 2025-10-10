from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd
from src import crud
from src.schemas import schemas_logic
from src.database import get_db

# Створення маршрутизатора для роботи з планами
router = APIRouter(tags=["Plans"])


@router.post(
    "/plans_insert",
    response_model=schemas_logic.PlanInsertResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_plans(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    📌 Endpoint для імпорту планів із Excel файлу.

    - **file**: Excel файл з колонками `period`, `category_name`, `sum`
    - **db**: підключення до бази даних (Session)

    Процес:
    1. Читає Excel файл у pandas DataFrame.
    2. Перевіряє наявність обов'язкових колонок.
    3. Створює список об'єктів PlanInsertItem для кожного рядка.
    4. Викликає функцію crud.insert_plans для додавання даних у базу.

    Повертає:
    - Об'єкт PlanInsertResponse з інформацією про додані плани.

    Помилки:
    - HTTP 400: якщо файл не Excel або не має потрібних колонок.
    """
    try:
        # Читання Excel файлу у DataFrame
        df = pd.read_excel(file.file)
    except Exception:
        # Повертаємо помилку, якщо файл некоректний
        raise HTTPException(status_code=400, detail="Invalid Excel file")

    # Перевірка наявності обов'язкових колонок
    required_cols = {"period", "category_name", "sum"}
    if not required_cols.issubset(df.columns):
        raise HTTPException(
            status_code=400, detail=f"Excel must have columns: {required_cols}"
        )

    # Створення списку об'єктів PlanInsertItem для вставки в базу
    plan_items = [
        schemas_logic.PlanInsertItem(
            period=row["period"], category_name=row["category_name"], sum=row["sum"]
        )
        for _, row in df.iterrows()
    ]

    # Виклик CRUD-функції для збереження планів у базі
    return crud.insert_plans(db, plan_items)
