from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.refresh_token import RefreshToken

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    def by_username(self, username: str):
        return self.db.scalar(select(User).where(User.username == username))
    def by_email(self, email: str):
        return self.db.scalar(select(User).where(User.email == email))
    def by_id(self, user_id: int):
        return self.db.get(User, user_id)
    def list(self):
        return list(self.db.scalars(select(User).order_by(User.id)))
    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    def refresh_by_jti(self, jti: str):
        return self.db.scalar(select(RefreshToken).where(RefreshToken.jti == jti))
