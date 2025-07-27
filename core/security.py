from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi import HTTPException

from core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed: str):
    return pwd_context.verify(plain_password, hashed)

# JWT token creation (for access/refresh tokens)
def create_token(data: dict, expires_delta: timedelta, token_type: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str, expected_type: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != expected_type:
            raise JWTError("Invalid token type")
        return payload
    except JWTError:
        return None

# -------------------------------
# Invite Token (itsdangerous)
# -------------------------------

# Initialize serializer with secret key
serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

def generate_invite_token(email: str, expires_sec: int = 86400) -> str:
    """Create an invite token that expires after `expires_sec` seconds (default: 24h)."""
    return serializer.dumps(email, salt="invite")

def verify_invite_token(token: str, max_age: int = 86400) -> str:
    """Verify the invite token within `max_age` limit."""
    try:
        return serializer.loads(token, salt="invite", max_age=max_age)
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Invite token expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid invite token")
