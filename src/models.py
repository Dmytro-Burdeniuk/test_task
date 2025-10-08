from sqlalchemy import Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    login: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    registration_date: Mapped[Date] = mapped_column(Date, nullable=False)

    credits: Mapped[list["Credit"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Credit(Base):
    __tablename__ = "Credits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("Users.id", ondelete="SET NULL"), nullable=True)
    issuance_date: Mapped[Date] = mapped_column(Date, nullable=False)
    return_date: Mapped[Date] = mapped_column(Date, nullable=False)
    actual_return_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    body: Mapped[float] = mapped_column(Float, nullable=False)
    percent: Mapped[float] = mapped_column(Float, nullable=False)

    user: Mapped["User"] = relationship(back_populates="credits")
    payments: Mapped[list["Payment"]] = relationship(back_populates="credit", cascade="all, delete-orphan")


class Dictionary(Base):
    __tablename__ = "Dictionary"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


class Plan(Base):
    __tablename__ = "Plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    period: Mapped[Date] = mapped_column(Date, nullable=False)
    sum: Mapped[float] = mapped_column(Float, nullable=False)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("Dictionary.id", ondelete="SET NULL"), nullable=True)

    category: Mapped["Dictionary"] = relationship()


class Payment(Base):
    __tablename__ = "Payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sum: Mapped[float] = mapped_column(Float, nullable=False)
    payment_date: Mapped[Date] = mapped_column(Date, nullable=False)
    credit_id: Mapped[int | None] = mapped_column(ForeignKey("Credits.id", ondelete="SET NULL"), nullable=True)
    type_id: Mapped[int | None] = mapped_column(ForeignKey("Dictionary.id", ondelete="SET NULL"), nullable=True)

    credit: Mapped["Credit"] = relationship(back_populates="payments")
    type: Mapped["Dictionary"] = relationship()
