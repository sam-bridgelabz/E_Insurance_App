from app.auth.oauth2 import get_current_user
from fastapi import Depends, HTTPException, status


def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have the permission to perform this action.",
        )

    return current_user


def employee_required(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "employee" or current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Employees only.",
        )
    return current_user
