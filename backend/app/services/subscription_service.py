from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.core.plans import PLANS


def create_subscription_for_company(db: Session, company_id: str, plan: str):
    plan_data = PLANS.get(plan)

    if not plan_data:
        raise ValueError("Invalid plan")

    subscription = Subscription(
        company_id=company_id,
        plan=plan,
        staff_limit=plan_data["staff_limit"],
        status="active",
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    return subscription


def update_subscription_plan(db: Session, company_id: str, plan: str):
    subscription = (
        db.query(Subscription)
        .filter(Subscription.company_id == company_id)
        .first()
    )

    if not subscription:
        raise ValueError("Subscription not found")

    plan_data = PLANS.get(plan)
    if not plan_data:
        raise ValueError("Invalid plan")

    subscription.plan = plan
    subscription.staff_limit = plan_data["staff_limit"]

    db.commit()
    return subscription