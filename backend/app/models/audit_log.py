from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    company_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), index=True, nullable=False)

    action = Column(String, nullable=False)  # create | update | delete | login | generate_payroll
    entity = Column(String, nullable=False)  # staff | roster | payroll | shift
    entity_id = Column(UUID(as_uuid=True), nullable=True)

    metadata = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())