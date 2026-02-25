from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    Boolean,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.session import Base


class PayrollPeriod(Base):
    __tablename__ = "payroll_periods"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    is_locked = Column(Boolean, default=False)

    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("company_id", "month", "year", name="unique_company_month_year"),
    )

    company = relationship("Company")


class PayrollRecord(Base):
    __tablename__ = "payroll_records"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    payroll_period_id = Column(Integer, ForeignKey("payroll_periods.id", ondelete="CASCADE"), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)

    total_hours = Column(Numeric(10, 2), nullable=False)
    salary_amount = Column(Numeric(12, 2), nullable=False)

    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("payroll_period_id", "staff_id", name="unique_staff_payroll"),
    )

    company = relationship("Company")
    payroll_period = relationship("PayrollPeriod")
    staff = relationship("Staff")