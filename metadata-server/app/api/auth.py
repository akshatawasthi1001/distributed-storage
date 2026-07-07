from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user_schema import (
    UserRegister,
    UserLogin
)
from app.services.auth_service import (
    register_user,
    login_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    return register_user(user, db)


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    return login_user(user, db)