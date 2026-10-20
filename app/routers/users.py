from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import authenticated, admin_only
from app.models.user import User
from app.schemas.auth import UserOut, RoleUpdate, StatusUpdate
from app.services.users import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(authenticated)):
    return user

@router.get("", response_model=list[UserOut], dependencies=[Depends(admin_only)])
def list_users(db: Session = Depends(get_db)):
    return UserService(db).list_users()

@router.patch("/{user_id}/role", response_model=UserOut)
def update_role(user_id: int, data: RoleUpdate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return UserService(db).update_role(user_id, data.role)

@router.patch("/{user_id}/status", response_model=UserOut)
def update_status(user_id: int, data: StatusUpdate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return UserService(db).update_status(user_id, data.is_active)
