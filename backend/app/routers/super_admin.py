from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.session import get_db
from app.models.company import Company
from app.models.subscription import Subscription
from app.models.user import User
from app.models.audit_log import AuditLog
from app.core.rbac import require_roles

router = APIRouter(prefix="/super-admin", tags=["Super Admin"])


# ======================================================
# DASHBOARD STATS
# ======================================================

@router.get("/dashboard", dependencies=[Depends(require_roles("super_admin"))])
def dashboard_stats(db: Session = Depends(get_db)):

    total_companies = db.query(Company).count()
    total_users = db.query(User).count()
    active_subscriptions = (
        db.query(Subscription)
        .filter(Subscription.status == "active")
        .count()
    )

    return {
        "total_companies": total_companies,
        "total_users": total_users,
        "active_subscriptions": active_subscriptions,
    }


# ======================================================
# LIST ALL COMPANIES
# ======================================================

@router.get("/companies", dependencies=[Depends(require_roles("super_admin"))])
def list_companies(db: Session = Depends(get_db)):

    companies = db.query(Company).all()

    result = []

    for company in companies:
        subscription = (
            db.query(Subscription)
            .filter(Subscription.company_id == company.id)
            .first()
        )

        result.append({
            "id": company.id,
            "name": company.name,
            "subscription_status": subscription.status if subscription else "none",
        })

    return result


# ======================================================
# SUSPEND COMPANY
# ======================================================

@router.post("/companies/{company_id}/suspend",
             dependencies=[Depends(require_roles("super_admin"))])
def suspend_company(company_id: UUID, db: Session = Depends(get_db)):

    subscription = (
        db.query(Subscription)
        .filter(Subscription.company_id == company_id)
        .first()
    )

    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    subscription.status = "canceled"
    db.commit()

    return {"message": "Company suspended"}


# ======================================================
# VIEW GLOBAL AUDIT LOGS
# ======================================================

@router.get("/audit-logs", dependencies=[Depends(require_roles("super_admin"))])
def global_audit_logs(db: Session = Depends(get_db)):

    logs = (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .limit(200)
        .all()
    )

    return logs