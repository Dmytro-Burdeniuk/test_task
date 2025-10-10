from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import date
from src import crud
from src.schemas import schemas_logic
from src.database import get_db

router = APIRouter(tags=["Reports"])


@router.get(
    "/plans_performance",
    response_model=schemas_logic.PlansPerformanceResponse,
    status_code=status.HTTP_200_OK,
)
def plans_performance(target_date: date, db: Session = Depends(get_db)):
    """Виконання планів до певної дати"""
    return crud.get_plans_performance(db, target_date)


@router.get(
    "/year_performance",
    response_model=schemas_logic.YearPerformanceResponse,
    status_code=status.HTTP_200_OK,
)
def year_performance(year: int, db: Session = Depends(get_db)):
    """Річний звіт по місяцях"""
    return crud.get_year_performance(db, year)
