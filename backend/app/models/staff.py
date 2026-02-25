from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Numeric,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.session import Base


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

    full_name = Column(String(255), nullable=False)
    position = Column(String(100), nullable=False)  # manager | service | kitchen | admin

    phone = Column(String(50))
    email = Column(String(255))
    address = Column(String)

    salary_type = Column(String(50), nullable=False)  # hourly | package
    hourly_rate = Column(Numeric(10, 2))
    package_salary = Column(Numeric(10, 2))

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company")