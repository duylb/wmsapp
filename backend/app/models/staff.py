from sqlalchemy import Column, String, Float, Boolean
from app.models.base import TenantBase


class Staff(TenantBase):
    __tablename__ = "staff"

    full_name = Column(String, nullable=False)
    position = Column(String, nullable=False)

    salary_type = Column(String, nullable=False)  # hourly | package
    hourly_rate = Column(Float, nullable=True)
    package_salary = Column(Float, nullable=True)

    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)