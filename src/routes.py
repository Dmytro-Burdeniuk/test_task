from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
import pandas as pd

from src import crud, schemas_base, schemas_logic
from src.database import get_db

router = APIRouter()


@router.get("/user_credits/{user_id}", response_model=schemas_logic.UserCreditsResponse, status_code=status.HTTP_200_OK)
def read_user_credits(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_credits(db, user_id)


@router.post("/plans_insert", response_model=schemas_logic.PlanInsertResponse, status_code=status.HTTP_201_CREATED)
def upload_plans(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = pd.read_excel(file.file)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Excel file")

    required_cols = {"period", "category_name", "sum"}
    if not required_cols.issubset(df.columns):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Excel must have columns: {required_cols}")

    plan_items = [
        schemas_logic.PlanInsertItem(
            period=row["period"],
            category_name=row["category_name"],
            sum=row["sum"]
        )
        for _, row in df.iterrows()
    ]
    return crud.insert_plans(db, plan_items)


@router.get("/plans_performance", response_model=schemas_logic.PlansPerformanceResponse, status_code=status.HTTP_200_OK)
def plans_performance(target_date: date, db: Session = Depends(get_db)):
    return crud.get_plans_performance(db, target_date)


@router.get("/year_performance", response_model=schemas_logic.YearPerformanceResponse, status_code=status.HTTP_200_OK)
def year_performance(year: int, db: Session = Depends(get_db)):
    return crud.get_year_performance(db, year)
