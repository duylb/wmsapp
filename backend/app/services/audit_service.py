from sqlalchemy.orm import Session
from uuid import UUID
import json

from app.models.audit_log import AuditLog


def log_action(
    db: Session,
    *,
    company_id: UUID,
    user_id: UUID,
    action: str,
    entity: str,
    entity_id: UUID | None = None,
    metadata: dict | None = None,
):
    audit = AuditLog(
        company_id=company_id,
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        metadata=json.dumps(metadata) if metadata else None,
    )

    db.add(audit)
    db.commit()