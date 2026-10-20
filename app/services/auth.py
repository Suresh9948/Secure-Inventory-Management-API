from datetime import datetime, timezone
from fastapi import HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.models.user import User, UserRole
from app.models.refresh_token import RefreshToken
from app.repositories.users import UserRepository

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def register(self, username: str, email: str, password: str):
        if self.repo.by_username(username):
            raise HTTPException(status_code=409, detail="Username already exists")
        if self.repo.by_email(email):
            raise HTTPException(status_code=409, detail="Email already exists")
        user = User(username=username, email=email, hashed_password=hash_password(password), role=UserRole.EMPLOYEE, is_active=True)
        return self.repo.create(user)

    def login(self, username: str, password: str):
        user = self.repo.by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid username or password", headers={"WWW-Authenticate": "Bearer"})
        if not user.is_active:
            raise HTTPException(status_code=401, detail="Account is inactive")
        access, expires_in = create_access_token(user.id, user.role.value)
        refresh, jti, expires = create_refresh_token(user.id)
        now = datetime.now(timezone.utc)
        self.db.add(RefreshToken(jti=jti, user_id=user.id, expires_at=expires, revoked=False, created_at=now))
        self.db.commit()
        return {"access_token": access, "refresh_token": refresh, "token_type": "bearer", "expires_in": expires_in}

    def refresh(self, raw_token: str):
        try:
            payload = jwt.decode(raw_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            if payload.get("type") != "refresh" or not payload.get("sub") or not payload.get("jti"):
                raise ValueError()
            user_id, jti = int(payload["sub"]), payload["jti"]
        except (JWTError, ValueError, TypeError, KeyError):
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        record = self.repo.refresh_by_jti(jti)
        user = self.repo.by_id(user_id)
        now = datetime.now(timezone.utc)
        expiry = record.expires_at.replace(tzinfo=timezone.utc) if record and record.expires_at.tzinfo is None else (record.expires_at if record else now)
        if not record or record.revoked or record.user_id != user_id or expiry <= now or not user or not user.is_active:
            raise HTTPException(status_code=401, detail="Refresh token is invalid, expired, or revoked")
        record.revoked = True
        access, expires_in = create_access_token(user.id, user.role.value)
        refresh, new_jti, new_expiry = create_refresh_token(user.id)
        self.db.add(RefreshToken(jti=new_jti, user_id=user.id, expires_at=new_expiry, revoked=False, created_at=now))
        self.db.commit()
        return {"access_token": access, "refresh_token": refresh, "token_type": "bearer", "expires_in": expires_in}

    def logout(self, raw_token: str):
        try:
            payload = jwt.decode(raw_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            if payload.get("type") != "refresh" or not payload.get("jti"):
                raise ValueError()
        except (JWTError, ValueError, TypeError, KeyError):
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        record = self.repo.refresh_by_jti(payload["jti"])
        if not record or record.revoked:
            raise HTTPException(status_code=401, detail="Refresh token is invalid or already revoked")
        record.revoked = True
        self.db.commit()
