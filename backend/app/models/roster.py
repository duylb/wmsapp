from sqlalchemy import (
    Column,
    Integer,
    Date,
    ForeignKey,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.session import Base


class Roster(Base):
    __tablename__ = "rosters"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

    staff_id = Column(Integer, ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)

    morning_shift_id = Column(Integer, ForeignKey("shifts.id"))
    afternoon_shift_id = Column(Integer, ForeignKey("shifts.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("company_id", "staff_id", "date", name="unique_staff_date"),
    )

    company = relationship("Company")
    staff = relationship("Staff")