from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import date
from src import crud
from src.schemas import schemas_logic
from src.database import get_db

# Створення маршрутизатора для звітів
router = APIRouter(tags=["Reports"])


@router.get(
    "/plans_performance",
    response_model=schemas_logic.PlansPerformanceResponse,
    status_code=status.HTTP_200_OK,
)
def plans_performance(target_date: date, db: Session = Depends(get_db)):
    """
    Endpoint для отримання інформації про виконання планів станом на певну дату.

    - **target_date**: дата, до якої потрібно перевірити виконання планів
    - **db**: підключення до бази даних (Session)

    Повертає:
    - Список планів з наступною інформацією:
        - Місяць плану (`period`)
        - Категорія плану (`category_name`)
        - Запланована сума (`planned_sum`)
        - Фактична сума виданих кредитів або платежів (`actual_sum`)
        - % виконання плану (`performance_percent`)

    Використовує CRUD-функцію `get_plans_performance` для отримання даних.
    """
    return crud.get_plans_performance(db, target_date)


@router.get(
    "/year_performance",
    response_model=schemas_logic.YearPerformanceResponse,
    status_code=status.HTTP_200_OK,
)
def year_performance(year: int, db: Session = Depends(get_db)):
    """
    Endpoint для отримання річного звіту по місяцях.

    - **year**: рік для генерації звіту
    - **db**: підключення до бази даних (Session)

    Повертає:
    - Список по місяцях з наступною інформацією:
        - Місяць та рік (`period`)
        - Кількість видач та платежів (`credits_count`, `payments_count`)
        - Планові суми видач і збору (`plan_issue_sum`, `plan_collect_sum`)
        - Фактичні суми видач і збору (`actual_issue_sum`, `actual_collect_sum`)
        - % виконання планів (`issue_performance_percent`, `collect_performance_percent`)
        - % від річної суми (`issue_share_percent`, `collect_share_percent`)

    Використовує CRUD-функцію `get_year_performance` для отримання даних.
    """
    return crud.get_year_performance(db, year)
