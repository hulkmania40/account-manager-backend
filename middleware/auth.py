from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_token
from db import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def require_auth(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token, expected_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await db.users.find_one({"email": payload.get("sub")})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def require_admin(user=Depends(require_auth)):
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin only")
    return user
