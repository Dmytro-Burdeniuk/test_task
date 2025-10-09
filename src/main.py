from fastapi import FastAPI
from src import routes, models
from src.database import engine

# Створення таблиць у БД, якщо їх ще немає
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Credits API")

# Підключаємо роутер
app.include_router(routes.router)
