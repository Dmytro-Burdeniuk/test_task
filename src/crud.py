from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date, timedelta
from typing import List

from src import models
from src.schemas import schemas_logic


def get_user_credits(db: Session, user_id: int) -> schemas_logic.UserCreditsResponse:
    """
    Повертає список кредитів для конкретного користувача.

    Аргументи:
    - db: сесія бази даних
    - user_id: ID користувача

    Повертає:
    - Список кредитів користувача з розділенням на відкриті та закриті:
        - Для відкритих: дні прострочки, сплачені тіло та відсотки
        - Для закритих: дата фактичного закриття та загальна сума платежів
    """
    credits = db.query(models.Credit).filter(models.Credit.user_id == user_id).all()
    response = []

    for c in credits:
        total_payments_sum = sum(p.sum for p in c.payments)
        body_sum = sum(p.sum for p in c.payments if p.type.name.lower() == "тіло")
        percent_sum = sum(
            p.sum for p in c.payments if p.type.name.lower() == "відсотки"
        )

        if c.actual_return_date:
            item = schemas_logic.UserCreditClosed(
                issuance_date=c.issuance_date,
                is_closed=True,
                body=c.body,
                percent=c.percent,
                actual_return_date=c.actual_return_date,
                total_payments_sum=total_payments_sum,
            )
        else:
            overdue_days = max((date.today() - c.return_date).days, 0)
            item = schemas_logic.UserCreditOpen(
                issuance_date=c.issuance_date,
                is_closed=False,
                body=c.body,
                percent=c.percent,
                return_date=c.return_date,
                overdue_days=overdue_days,
                body_payments_sum=body_sum,
                percent_payments_sum=percent_sum,
            )
        response.append(item)
    return response


def insert_plans(
    db: Session, plan_items: List[schemas_logic.PlanInsertItem]
) -> schemas_logic.PlanInsertResponse:
    """
    Імпортує плани в базу даних із списку об'єктів.

    Аргументи:
    - db: сесія бази даних
    - plan_items: список планів для вставки (дата, категорія, сума)

    Логіка:
    - Пропускає плани, якщо категорія не знайдена
    - Пропускає плани, якщо вже існує запис з тією ж датою та категорією

    Повертає:
    - inserted_count: кількість успішно доданих планів
    - skipped: список пропущених записів
    - message: текстовий підсумок вставки
    """
    inserted_count = 0
    skipped = []

    for item in plan_items:
        category = (
            db.query(models.Dictionary)
            .filter(models.Dictionary.name == item.category_name)
            .first()
        )
        if not category:
            skipped.append(f"{item.period} - {item.category_name} (Category not found)")
            continue

        existing = (
            db.query(models.Plan)
            .filter(
                models.Plan.period == item.period,
                models.Plan.category_id == category.id,
            )
            .first()
        )
        if existing:
            skipped.append(f"{item.period} - {item.category_name}")
            continue

        plan = models.Plan(period=item.period, sum=item.sum, category_id=category.id)
        db.add(plan)
        inserted_count += 1

    db.commit()
    return schemas_logic.PlanInsertResponse(
        inserted_count=inserted_count,
        skipped=skipped,
        message=f"{inserted_count} plans inserted, {len(skipped)} skipped",
    )


def get_plans_performance(
    db: Session, target_date: date
) -> schemas_logic.PlansPerformanceResponse:
    """
    Повертає виконання планів до певної дати.

    Аргументи:
    - db: сесія бази даних
    - target_date: дата, до якої розраховується виконання планів

    Логіка:
    - Вибирає плани на місяць target_date
    - Для категорії "видача": сумує видані кредити
    - Для категорії "збір": сумує платежі
    - Розраховує % виконання плану

    Повертає:
    - Список елементів PlanPerformanceItem:
        - period: дата плану
        - category_name: назва категорії
        - planned_sum: сума плану
        - actual_sum: фактична сума
        - performance_percent: % виконання
    """
    plans = (
        db.query(models.Plan)
        .filter(
            extract("year", models.Plan.period) == target_date.year,
            extract("month", models.Plan.period) == target_date.month,
        )
        .all()
    )
    response = []

    for plan in plans:
        category_name = plan.category.name
        planned_sum = plan.sum
        if category_name.lower() == "видача":
            actual_sum = (
                db.query(func.sum(models.Credit.body))
                .filter(
                    models.Credit.issuance_date >= plan.period,
                    models.Credit.issuance_date <= target_date,
                )
                .scalar()
                or 0
            )
        else:
            actual_sum = (
                db.query(func.sum(models.Payment.sum))
                .join(models.Payment.type)
                .filter(
                    models.Payment.payment_date >= plan.period,
                    models.Payment.payment_date <= target_date,
                    models.Dictionary.name == category_name,
                )
                .scalar()
                or 0
            )

        percent = (actual_sum / planned_sum * 100) if planned_sum > 0 else 0

        response.append(
            schemas_logic.PlanPerformanceItem(
                period=plan.period,
                category_name=category_name,
                planned_sum=planned_sum,
                actual_sum=actual_sum,
                performance_percent=percent,
            )
        )
    return response


def get_year_performance(
    db: Session, year: int
) -> schemas_logic.YearPerformanceResponse:
    """
    Повертає річний звіт з групуванням по місяцях.

    Аргументи:
    - db: сесія бази даних
    - year: рік для звіту

    Логіка:
    - Розраховує кількість видач і суму за планом для кожного місяця
    - Розраховує кількість платежів і суму за планом по "збору"
    - Обчислює % виконання плану по місяцях
    - Обчислює частку видач і платежів цього місяця від річної суми

    Повертає:
    - Список YearPerformanceItem:
        - period: місяць.рік
        - credits_count: кількість видач
        - plan_issue_sum: сума плану по видачам
        - actual_issue_sum: фактична сума видач
        - issue_performance_percent: % виконання плану по видачам
        - payments_count: кількість платежів
        - plan_collect_sum: сума плану по збору
        - actual_collect_sum: фактична сума платежів
        - collect_performance_percent: % виконання плану по збору
        - issue_share_percent: % суми видач за місяць від річної суми
        - collect_share_percent: % суми платежів за місяць від річної суми
    """
    response = []

    total_issue_year = (
        db.query(func.sum(models.Credit.body))
        .filter(extract("year", models.Credit.issuance_date) == year)
        .scalar()
        or 1
    )
    total_collect_year = (
        db.query(func.sum(models.Payment.sum))
        .join(models.Payment.type)
        .filter(extract("year", models.Payment.payment_date) == year)
        .scalar()
        or 1
    )

    for month in range(1, 13):
        period_start = date(year, month, 1)
        period_end = (
            date(year, month + 1, 1) - timedelta(days=1)
            if month < 12
            else date(year, 12, 31)
        )

        credits_query = db.query(models.Credit).filter(
            models.Credit.issuance_date >= period_start,
            models.Credit.issuance_date <= period_end,
        )
        credits_count = credits_query.count()
        actual_issue_sum = (
            credits_query.with_entities(func.sum(models.Credit.body)).scalar() or 0
        )

        plan_issue_sum = (
            db.query(func.sum(models.Plan.sum))
            .join(models.Plan.category)
            .filter(
                extract("year", models.Plan.period) == year,
                extract("month", models.Plan.period) == month,
                models.Dictionary.name.ilike("%видача%"),
            )
            .scalar()
            or 0
        )

        issue_percent = (
            (actual_issue_sum / plan_issue_sum * 100) if plan_issue_sum else 0
        )
        issue_share = actual_issue_sum / total_issue_year * 100

        payments_query = (
            db.query(models.Payment)
            .join(models.Payment.type)
            .filter(
                models.Payment.payment_date >= period_start,
                models.Payment.payment_date <= period_end,
            )
        )
        payments_count = payments_query.count()
        actual_collect_sum = (
            payments_query.with_entities(func.sum(models.Payment.sum)).scalar() or 0
        )

        plan_collect_sum = (
            db.query(func.sum(models.Plan.sum))
            .join(models.Plan.category)
            .filter(
                extract("year", models.Plan.period) == year,
                extract("month", models.Plan.period) == month,
                models.Dictionary.name.ilike("%збір%"),
            )
            .scalar()
            or 0
        )

        collect_percent = (
            (actual_collect_sum / plan_collect_sum * 100) if plan_collect_sum else 0
        )
        collect_share = actual_collect_sum / total_collect_year * 100

        response.append(
            schemas_logic.YearPerformanceItem(
                period=f"{month:02d}.{year}",
                credits_count=credits_count,
                plan_issue_sum=plan_issue_sum,
                actual_issue_sum=actual_issue_sum,
                issue_performance_percent=issue_percent,
                payments_count=payments_count,
                plan_collect_sum=plan_collect_sum,
                actual_collect_sum=actual_collect_sum,
                collect_performance_percent=collect_percent,
                issue_share_percent=issue_share,
                collect_share_percent=collect_share,
            )
        )

    return response
