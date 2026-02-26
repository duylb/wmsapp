from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.session import get_db
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate, StaffResponse
from app.core.tenant import get_current_company_id
from app.dependencies.auth import get_current_user
from app.core.rbac import require_roles
from app.services.audit_service import log_action

router = APIRouter(prefix="/staff", tags=["Staff"])


# ============================================================
# LIST STAFF
# ============================================================

@router.get(
    "/",
    response_model=list[StaffResponse],
    dependencies=[Depends(require_roles("admin", "manager", "staff"))],
)
def list_staff(
    db: Session = Depends(get_db),
    company_id: UUID = Depends(get_current_company_id),
):
    staff = (
        db.query(Staff)
        .filter(
            Staff.company_id == company_id,
            Staff.is_active == True,
        )
        .all()
    )

    return staff


# ============================================================
# CREATE STAFF
# ============================================================

@router.post(
    "/",
    response_model=StaffResponse,
    dependencies=[Depends(require_roles("admin", "manager"))],
)
def create_staff(
    payload: StaffCreate,
    db: Session = Depends(get_db),
    company_id: UUID = Depends(get_current_company_id),
    current_user=Depends(get_current_user),
):
    staff = Staff(
        **payload.dict(),
        company_id=company_id,
    )

    db.add(staff)
    db.commit()
    db.refresh(staff)

    # Audit log
    log_action(
        db=db,
        company_id=company_id,
        user_id=current_user.id,
        action="create",
        entity="staff",
        entity_id=staff.id,
    )

    return staff


# ============================================================
# UPDATE STAFF
# ============================================================

@router.put(
    "/{staff_id}",
    response_model=StaffResponse,
    dependencies=[Depends(require_roles("admin", "manager"))],
)
def update_staff(
    staff_id: UUID,
    payload: StaffUpdate,
    db: Session = Depends(get_db),
    company_id: UUID = Depends(get_current_company_id),
    current_user=Depends(get_current_user),
):
    staff = (
        db.query(Staff)
        .filter(
            Staff.id == staff_id,
            Staff.company_id == company_id,
        )
        .first()
    )

    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found",
        )

    update_data = payload.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(staff, key, value)

    db.commit()
    db.refresh(staff)

    # Audit log
    log_action(
        db=db,
        company_id=company_id,
        user_id=current_user.id,
        action="update",
        entity="staff",
        entity_id=staff.id,
        metadata=update_data,
    )

    return staff


# ============================================================
# DEACTIVATE STAFF (SOFT DELETE)
# ============================================================

@router.delete(
    "/{staff_id}",
    dependencies=[Depends(require_roles("admin"))],
)
def deactivate_staff(
    staff_id: UUID,
    db: Session = Depends(get_db),
    company_id: UUID = Depends(get_current_company_id),
    current_user=Depends(get_current_user),
):
    staff = (
        db.query(Staff)
        .filter(
            Staff.id == staff_id,
            Staff.company_id == company_id,
        )
        .first()
    )

    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found",
        )

    staff.is_active = False

    db.commit()

    # Audit log
    log_action(
        db=db,
        company_id=company_id,
        user_id=current_user.id,
        action="deactivate",
        entity="staff",
        entity_id=staff.id,
    )

    return {"message": "Staff deactivated successfully"}