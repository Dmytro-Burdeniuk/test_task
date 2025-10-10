from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src import crud
from src.schemas import schemas_logic
from src.database import get_db

router = APIRouter(tags=["Users"])

@router.get(
    "/user_credits/{user_id}",
    response_model=schemas_logic.UserCreditsResponse,
    status_code=status.HTTP_200_OK
)
def read_user_credits(user_id: int, db: Session = Depends(get_db)):
    """Повертає кредити користувача"""
    return crud.get_user_credits(db, user_id)
