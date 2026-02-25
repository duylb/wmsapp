from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.session import Base


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

    name = Column(String(50), nullable=False)  # S1, S2, B1, etc.
    duration_hours = Column(Numeric(4, 2), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company")