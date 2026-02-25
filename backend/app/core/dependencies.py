def get_current_company(
    current_user: User = Depends(get_current_user)
):
    return current_user.company_id