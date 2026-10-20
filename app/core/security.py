from datetime import datetime, timedelta, timezone
from uuid import uuid4
from jose import jwt
from pwdlib import PasswordHash
from app.core.config import settings

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        return password_hash.verify(password, hashed)
    except Exception:
        return False

def create_access_token(user_id: int, role: str) -> tuple[str, int]:
    expires_in = settings.access_token_expire_minutes * 60
    expires = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    payload = {"sub": str(user_id), "role": role, "type": "access", "exp": expires, "jti": str(uuid4())}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm), expires_in

def create_refresh_token(user_id: int) -> tuple[str, str, datetime]:
    jti = str(uuid4())
    expires = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    payload = {"sub": str(user_id), "type": "refresh", "exp": expires, "jti": jti}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm), jti, expires
