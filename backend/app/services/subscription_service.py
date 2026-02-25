from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.subscription import Subscription


def get_subscription(db: Session, company_id: int):
    return db.query(Subscription).filter(
        Subscription.company_id == company_id
    ).first()


def create_subscription(db: Session, company_id: int, plan: str):
    existing = get_subscription(db, company_id)
    if existing:
        raise HTTPException(status_code=400, detail="Subscription already exists")

    subscription = Subscription(
        company_id=company_id,
        plan=plan,
        status="trial"
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    return subscription


def update_subscription_status(db: Session, company_id: int, status: str):
    subscription = get_subscription(db, company_id)

    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    subscription.status = status
    db.commit()
    db.refresh(subscription)

    return subscription