from fastapi import Depends, HTTPException, status

from app.auth.oauth2 import get_current_user


def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Admins only.",
        )

    return current_user


def employee_required(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "employee" and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Employees or Admins only.",
        )
    return current_user
