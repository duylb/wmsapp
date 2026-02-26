from sqlalchemy.orm import Session
from app.models.staff import Staff
from app.models.subscription import Subscription
from app.services.stripe_service import report_staff_usage


def create_staff(db: Session, company_id: str, data: dict):

    subscription = (
        db.query(Subscription)
        .filter(Subscription.company_id == company_id)
        .first()
    )

    staff = Staff(**data, company_id=company_id)

    db.add(staff)
    db.commit()
    db.refresh(staff)

    # Report usage increment (+1)
    if subscription and subscription.stripe_usage_item_id:
        report_staff_usage(subscription.stripe_usage_item_id, 1)

    return staff


def deactivate_staff(db: Session, company_id: str, staff_id: str):

    staff = (
        db.query(Staff)
        .filter(
            Staff.id == staff_id,
            Staff.company_id == company_id,
        )
        .first()
    )

    if not staff:
        raise Exception("Staff not found")

    staff.is_active = False
    db.commit()

    subscription = (
        db.query(Subscription)
        .filter(Subscription.company_id == company_id)
        .first()
    )

    # Optional: decrement usage (if using net usage model)
    if subscription and subscription.stripe_usage_item_id:
        report_staff_usage(subscription.stripe_usage_item_id, -1)

    return staff