from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import stripe

from app.database.session import get_db
from app.core.config import settings
from app.models.subscription import Subscription

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.post("/webhook")
async def stripe_webhook(request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    event = stripe.Webhook.construct_event(
        payload,
        sig_header,
        settings.STRIPE_WEBHOOK_SECRET,
    )

    if event["type"] == "customer.subscription.created":
        subscription_data = event["data"]["object"]

        company_id = subscription_data["metadata"]["company_id"]

        usage_item = None

        for item in subscription_data["items"]["data"]:
            if item["price"]["usage_type"] == "metered":
                usage_item = item["id"]

        db_subscription = (
            db.query(Subscription)
            .filter(Subscription.company_id == company_id)
            .first()
        )

        db_subscription.stripe_subscription_id = subscription_data["id"]
        db_subscription.stripe_usage_item_id = usage_item
        db_subscription.status = "active"

        db.commit()

    return {"status": "success"}