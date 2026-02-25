from fastapi import Depends, HTTPException, status
from app.dependencies.auth import get_current_user


def get_current_company_id(current_user=Depends(get_current_user)):
    """
    Extract company_id from authenticated user.
    Enforces strict tenant isolation.
    """

    if not current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not assigned to a company",
        )

    return current_user.company_id