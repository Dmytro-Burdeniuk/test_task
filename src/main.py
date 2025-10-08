from fastapi import FastAPI

app = FastAPI(title="API HTTP Service to interact DB")


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}
