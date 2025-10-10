from fastapi import FastAPI
from src.routes import router as api_router
from src import models
from src.database import engine

app = FastAPI(
    title="Credit Planner API",
    description="Система аналізу планів, видач та зборів кредитів",
    version="1.0.0",
)

# Підключення роутів
app.include_router(api_router)


# Створення таблиць тільки при прямому запуску, не при імпорті
if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
