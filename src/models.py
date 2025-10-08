from sqlalchemy import Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    login: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    registration_date: Mapped[Date] = mapped_column(Date, nullable=False)

    credits: Mapped[list["Credit"]] = relationship(back_populates="user")


class Credit(Base):
    __tablename__ = "Credits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    issuance_date: Mapped[Date] = mapped_column(Date)
    return_date: Mapped[Date] = mapped_column(Date)
    actual_return_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    body: Mapped[float] = mapped_column(Float)
    percent: Mapped[float] = mapped_column(Float)

    user: Mapped["User"] = relationship(back_populates="credits")
    payments: Mapped[list["Payment"]] = relationship(back_populates="credit")


class Dictionary(Base):
    __tablename__ = "Dictionary"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)


class Plan(Base):
    __tablename__ = "Plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    period: Mapped[Date] = mapped_column(Date)
    sum: Mapped[float] = mapped_column(Float)
    category_id: Mapped[int] = mapped_column(ForeignKey("Dictionary.id"))

    category: Mapped["Dictionary"] = relationship()


class Payment(Base):
    __tablename__ = "Payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sum: Mapped[float] = mapped_column(Float)
    payment_date: Mapped[Date] = mapped_column(Date)
    credit_id: Mapped[int] = mapped_column(ForeignKey("Credits.id"))
    type_id: Mapped[int] = mapped_column(ForeignKey("Dictionary.id"))

    credit: Mapped["Credit"] = relationship(back_populates="payments")
    type: Mapped["Dictionary"] = relationship()