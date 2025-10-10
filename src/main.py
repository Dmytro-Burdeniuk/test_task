from fastapi import FastAPI
from src.routes import router as api_router
from src import models
from src.database import engine

# Створення таблиць у БД, якщо їх ще немає
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Credit Planner API",
    description="Система аналізу планів, видач та зборів кредитів",
    version="1.0.0",
)

# Підключення роутів
app.include_router(api_router)
