from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class StaffCreate(BaseModel):
    full_name: str
    position: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    salary_type: str  # hourly | package
    hourly_rate: Optional[float] = None
    package_salary: Optional[float] = None


class StaffUpdate(BaseModel):
    full_name: Optional[str]
    position: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    address: Optional[str]
    salary_type: Optional[str]
    hourly_rate: Optional[float]
    package_salary: Optional[float]
    is_active: Optional[bool]


class StaffResponse(BaseModel):
    id: int
    full_name: str
    position: str
    phone: Optional[str]
    email: Optional[EmailStr]
    address: Optional[str]
    salary_type: str
    hourly_rate: Optional[float]
    package_salary: Optional[float]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True