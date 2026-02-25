from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.session import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), unique=True)

    plan = Column(String(50), nullable=False)  # starter | pro | enterprise
    status = Column(String(50), nullable=False)  # active | trial | canceled

    stripe_customer_id = Column(String(255))
    current_period_end = Column(DateTime)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company")