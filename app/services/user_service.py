from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.models.user import User


def create_user(
    db: Session,
    email: str,
    password: str
):
    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user is not None:
        return None

    user = User(
        email=email,
        password_hash=hash_password(password),
        role="user"
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except IntegrityError:
        db.rollback()
        return None

def login_user(
    db: Session,
    email: str,
    password: str
):
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        return None

    password_is_correct = verify_password(
        password,
        user.password_hash
    )

    if not password_is_correct:
        return None

    token = create_access_token(
        user.id,
        user.role
    )

    return token