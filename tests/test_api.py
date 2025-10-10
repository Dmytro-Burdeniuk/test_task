import io
from datetime import date, datetime
import pandas as pd
import pytest
from fastapi.testclient import TestClient
from src.main import app  

client = TestClient(app)


def test_read_user_credits_returns_valid_response(monkeypatch):
    # Мок функції CRUD, повертаємо всі обов'язкові поля
    monkeypatch.setattr(
        "src.crud.get_user_credits",
        lambda db, user_id: [
            {
                "user_id": 1,
                "credits": [
                    {
                        "id": 1,
                        "amount": 1000,
                        "status": "issued",
                        "issuance_date": date.today(),
                        "is_closed": False,
                        "body": 1000,
                        "percent": 0,
                        "actual_return_date": None,
                        "total_payments_sum": 0,
                        "return_date": None,
                        "overdue_days": 0,
                        "body_payments_sum": 0,
                        "percent_payments_sum": 0,
                    }
                ],
            }
        ]
    )

    response = client.get("/user_credits/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == 1
    assert data[0]["credits"][0]["amount"] == 1000


def test_upload_plans_excel(monkeypatch):
    # Створюємо тестовий Excel файл
    df = pd.DataFrame({
        "period": [date(2025, 1, 1), date(2025, 2, 1)],
        "category_name": ["cat1", "cat2"],
        "sum": [1000, 2000]
    })
    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)

    # Мок insert_plans, повертаємо поля відповідно до response_model
    monkeypatch.setattr(
        "src.crud.insert_plans",
        lambda db, plan_items: {"inserted_count": len(plan_items), "message": "success"}
    )

    response = client.post(
        "/plans_insert",
        files={"file": ("test.xlsx", excel_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["inserted_count"] == 2
    assert data["message"] == "success"


def test_plans_performance(monkeypatch):
    # Мок функції CRUD
    monkeypatch.setattr(
        "src.crud.get_plans_performance",
        lambda db, target_date: [
            {
                "period": date(2025, 1, 1),
                "category_name": "cat1",
                "credits_count": 1,
                "planned_sum": 1000,
                "actual_sum": 500,
                "performance_percent": 50.0,
                "plan_issue_sum": 1000,
                "actual_issue_sum": 500,
                "issue_performance_percent": 50.0,
                "payments_count": 1,
                "plan_collect_sum": 2000,
                "actual_collect_sum": 1500,
                "collect_performance_percent": 75.0,
                "issue_share_percent": 10.0,
                "collect_share_percent": 15.0
            }
        ]
    )

    response = client.get(f"/plans_performance?target_date={date.today()}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["category_name"] == "cat1"
    assert data[0]["performance_percent"] == 50.0


def test_year_performance(monkeypatch):
    # Просто мок для перевірки проходження
    monkeypatch.setattr(
        "src.crud.get_year_performance",
        lambda db, year: {"total_credits": 10, "total_payments": 8000}
    )

    response = client.get("/year_performance?year=2025")
    assert response.status_code == 200
    data = response.json()
    assert data["total_credits"] == 10
    assert data["total_payments"] == 8000
