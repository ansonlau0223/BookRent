from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse
)

from app.services.user_service import (
    create_user,
    login_user
)

from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register_user(
    request: UserRegister,
    db: Session = Depends(get_db)
):
    user = create_user(
        db,
        request.email,
        request.password
    )

    if user is None:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    return user

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    request: UserLogin,
    db: Session = Depends(get_db)
):
    token = login_user(
        db,
        request.email,
        request.password
    )

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(
        get_current_user
    )
):
    return current_user