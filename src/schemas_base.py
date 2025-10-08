from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# Schemas to align input and output data with DB structure


class UserBase(BaseModel):
    login: str = Field(..., max_length=100)
    registration_date: date


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)  


class CreditBase(BaseModel):
    issuance_date: date
    return_date: date
    actual_return_date: Optional[date] = None
    body: float
    percent: float
    user_id: int


class CreditCreate(CreditBase):
    pass


class CreditRead(CreditBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class DictionaryBase(BaseModel):
    name: str = Field(..., max_length=255)


class DictionaryCreate(DictionaryBase):
    pass


class DictionaryRead(DictionaryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PlanBase(BaseModel):
    period: date
    sum: float
    category_id: int


class PlanCreate(PlanBase):
    pass


class PlanRead(PlanBase):
    id: int
    category: Optional[DictionaryRead] = None
    model_config = ConfigDict(from_attributes=True)


class PaymentBase(BaseModel):
    sum: float
    payment_date: date
    credit_id: int
    type_id: int


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    id: int
    type: Optional[DictionaryRead] = None
    model_config = ConfigDict(from_attributes=True)