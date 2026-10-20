from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.users import UserRepository
from app.models.user import UserRole

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)
    def list_users(self):
        return self.repo.list()
    def update_role(self, user_id: int, role: UserRole):
        user = self.repo.by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.role = role
        self.db.commit()
        self.db.refresh(user)
        return user
    def update_status(self, user_id: int, is_active: bool):
        user = self.repo.by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_active = is_active
        if not is_active:
            for token in user.refresh_tokens:
                token.revoked = True
        self.db.commit()
        self.db.refresh(user)
        return user
