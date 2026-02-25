from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.subscription import SubscriptionResponse
from app.services.subscription_service import (
    get_subscription,
    create_subscription,
)
from backend.app.core.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=SubscriptionResponse | None)
def my_subscription(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_subscription(db, current_user.company_id)


@router.post("/", response_model=SubscriptionResponse)
def create_new_subscription(
    plan: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_subscription(
        db,
        current_user.company_id,
        plan
    )