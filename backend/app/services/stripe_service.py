import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def report_staff_usage(stripe_subscription_id: str, quantity: int):
    """
    Report usage to Stripe (metered billing)
    """

    stripe.SubscriptionItem.create_usage_record(
        stripe_subscription_id,
        quantity=quantity,
        timestamp="now",
        action="increment",
    )