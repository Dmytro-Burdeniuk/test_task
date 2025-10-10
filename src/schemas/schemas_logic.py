from datetime import date
from typing import Optional, List, Union
from pydantic import BaseModel, Field, ConfigDict


# Схеми для коректного відпрацьовування бізнес логіки


# /user_credits/{user_id}
class UserCreditBase(BaseModel):
    issuance_date: date = Field(..., description="Дата видачі кредиту")
    is_closed: bool = Field(..., description="Чи закритий кредит (true/false)")
    body: float = Field(..., description="Сума видачі")
    percent: float = Field(..., description="Нараховані відсотки")


class UserCreditClosed(UserCreditBase):
    """Інформація про закритий кредит"""
    actual_return_date: date = Field(..., description="Дата фактичного повернення кредиту")
    total_payments_sum: float = Field(..., description="Сума всіх платежів за кредитом")


class UserCreditOpen(UserCreditBase):
    """Інформація про відкритий кредит"""
    return_date: date = Field(..., description="Крайня дата повернення кредиту")
    overdue_days: int = Field(..., description="Кількість днів прострочення")
    body_payments_sum: float = Field(..., description="Сума платежів по тілу")
    percent_payments_sum: float = Field(..., description="Сума платежів по відсотках")


UserCreditsResponse = List[Union[UserCreditClosed, UserCreditOpen]]


# /plans_insert
class PlanInsertItem(BaseModel):
    """Один запис із Excel-файлу (вхід)"""
    period: date = Field(..., description="Місяць плану (1 число місяця)")
    category_name: str = Field(..., description="Назва категорії (видача / збір)")
    sum: float = Field(..., ge=0, description="Сума за планом (0 допустиме значення)")


class PlanInsertResponse(BaseModel):
    """Вихід після імпорту планів"""
    inserted_count: int
    skipped: List[str] = Field(default_factory=list, description="Плани, що вже були у БД")
    message: str


# /plans_performance 
class PlanPerformanceItem(BaseModel):
    period: date
    category_name: str
    planned_sum: float
    actual_sum: float
    performance_percent: float


PlansPerformanceResponse = List[PlanPerformanceItem]


# /year_performance
class YearPerformanceItem(BaseModel):
    period: str = Field(..., description="Місяць і рік (формат MM.YYYY)")

    credits_count: int
    plan_issue_sum: float
    actual_issue_sum: float
    issue_performance_percent: float

    payments_count: int
    plan_collect_sum: float
    actual_collect_sum: float
    collect_performance_percent: float

    issue_share_percent: float
    collect_share_percent: float


YearPerformanceResponse = List[YearPerformanceItem]
