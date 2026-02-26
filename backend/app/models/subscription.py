import uuid
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    company_id = Column(UUID(as_uuid=True), index=True, nullable=False)

    stripe_subscription_id = Column(String, nullable=True)
    stripe_usage_item_id = Column(String, nullable=True)

    plan = Column(String, default="starter")

    status = Column(String, default="trialing")

    staff_limit = Column(Integer, default=5)

    trial_end = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())