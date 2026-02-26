from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.tenant import get_current_company_id
from app.tasks.payroll_tasks import generate_payroll_task
from app.core.rbac import require_roles

router = APIRouter(prefix="/payroll", tags=["Payroll"])


@router.post("/generate",
             dependencies=[Depends(require_roles("admin", "manager"))])
def generate_payroll(company_id=Depends(get_current_company_id)):
    generate_payroll_task.delay(str(company_id))
    return {"message": "Payroll generation started"}