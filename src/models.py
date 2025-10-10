from sqlalchemy import Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class User(Base):
    """
    Модель користувача

    Атрибути:
    - id: Унікальний ідентифікатор користувача
    - login: Логін користувача (унікальний)
    - registration_date: Дата реєстрації користувача
    - credits: Список кредитів користувача (один-до-багатьох)
    """

    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    login: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    registration_date: Mapped[Date] = mapped_column(Date, nullable=False)

    credits: Mapped[list["Credit"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Credit(Base):
    """
    Модель кредиту

    Атрибути:
    - id: Унікальний ідентифікатор кредиту
    - user_id: ID користувача, якому видано кредит (nullable)
    - issuance_date: Дата видачі кредиту
    - return_date: Планова дата повернення кредиту
    - actual_return_date: Фактична дата повернення (nullable)
    - body: Сума тіла кредиту
    - percent: Сума відсотків
    - user: Зв'язок з користувачем
    - payments: Список платежів по кредиту
    """

    __tablename__ = "Credits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("Users.id", ondelete="SET NULL"), nullable=True
    )
    issuance_date: Mapped[Date] = mapped_column(Date, nullable=False)
    return_date: Mapped[Date] = mapped_column(Date, nullable=False)
    actual_return_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    body: Mapped[float] = mapped_column(Float, nullable=False)
    percent: Mapped[float] = mapped_column(Float, nullable=False)

    user: Mapped["User"] = relationship(back_populates="credits")
    payments: Mapped[list["Payment"]] = relationship(
        back_populates="credit", cascade="all, delete-orphan"
    )


class Dictionary(Base):
    """
    Модель довідника

    Використовується для категорій планів та типів платежів.

    Атрибути:
    - id: Унікальний ідентифікатор запису
    - name: Назва категорії або типу (унікальна)
    """

    __tablename__ = "Dictionary"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


class Plan(Base):
    """
    Модель плану

    Атрибути:
    - id: Унікальний ідентифікатор плану
    - period: Дата/місяць плану
    - sum: Запланована сума
    - category_id: ID категорії з Dictionary
    - category: Зв'язок з категорією
    """

    __tablename__ = "Plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    period: Mapped[Date] = mapped_column(Date, nullable=False)
    sum: Mapped[float] = mapped_column(Float, nullable=False)
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("Dictionary.id", ondelete="SET NULL"), nullable=True
    )

    category: Mapped["Dictionary"] = relationship()


class Payment(Base):
    """
    Модель платежу

    Атрибути:
    - id: Унікальний ідентифікатор платежу
    - sum: Сума платежу
    - payment_date: Дата платежу
    - credit_id: ID кредиту (nullable)
    - type_id: ID типу платежу з Dictionary (nullable)
    - credit: Зв'язок з кредитом
    - type: Зв'язок з типом платежу
    """

    __tablename__ = "Payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sum: Mapped[float] = mapped_column(Float, nullable=False)
    payment_date: Mapped[Date] = mapped_column(Date, nullable=False)
    credit_id: Mapped[int | None] = mapped_column(
        ForeignKey("Credits.id", ondelete="SET NULL"), nullable=True
    )
    type_id: Mapped[int | None] = mapped_column(
        ForeignKey("Dictionary.id", ondelete="SET NULL"), nullable=True
    )

    credit: Mapped["Credit"] = relationship(back_populates="payments")
    type: Mapped["Dictionary"] = relationship()
