from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src import crud
from src.schemas import schemas_logic
from src.database import get_db

# Створення маршрутизатора для користувачів
router = APIRouter(tags=["Users"])


@router.get(
    "/user_credits/{user_id}",
    response_model=schemas_logic.UserCreditsResponse,
    status_code=status.HTTP_200_OK,
)
def read_user_credits(user_id: int, db: Session = Depends(get_db)):
    """
    Endpoint для отримання списку кредитів певного користувача.

    - **user_id**: ID користувача, для якого повертаються кредити
    - **db**: підключення до бази даних (Session)

    Повертає:
    - Список кредитів користувача з детальною інформацією про кожен кредит:
        - ID кредиту
        - Дата видачі
        - Сума кредиту
        - Інші пов’язані поля (залежить від моделі Credit)

    Використовує CRUD-функцію `get_user_credits` для отримання даних з бази.
    """
    return crud.get_user_credits(db, user_id)
