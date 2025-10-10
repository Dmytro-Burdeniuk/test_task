from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd
from src import crud
from src.schemas import schemas_logic
from src.database import get_db

router = APIRouter(tags=["Plans"])


@router.post(
    "/plans_insert",
    response_model=schemas_logic.PlanInsertResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_plans(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Імпорт планів із Excel"""
    try:
        df = pd.read_excel(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Excel file")

    required_cols = {"period", "category_name", "sum"}
    if not required_cols.issubset(df.columns):
        raise HTTPException(
            status_code=400, detail=f"Excel must have columns: {required_cols}"
        )

    plan_items = [
        schemas_logic.PlanInsertItem(
            period=row["period"], category_name=row["category_name"], sum=row["sum"]
        )
        for _, row in df.iterrows()
    ]
    return crud.insert_plans(db, plan_items)
