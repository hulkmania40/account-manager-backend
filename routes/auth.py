from fastapi import APIRouter, HTTPException, Depends
from schemas.user import LoginRequest, SignupRequest, TokenResponse
from core.security import hash_password, verify_password, create_token, decode_token
from db import db
from datetime import timedelta
from core.config import settings

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    user = await db.users.find_one({"email": req.email})
    if not user or not verify_password(req.password, user["hashed_password"]):
        raise HTTPException(401, detail="Invalid credentials")
    token = create_token({"sub": req.email}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), "access")
    return {"access_token": token}

@router.post("/signup")
async def signup(req: SignupRequest):
    payload = decode_token(req.token, expected_type="invite")
    if not payload:
        raise HTTPException(400, detail="Invalid or expired invite token")
    
    email = payload.get("sub")
    existing = await db.users.find_one({"email": email})
    if existing:
        raise HTTPException(400, detail="User already exists")

    invite = await db.invites.find_one({"email": email, "token": req.token, "used": False})
    if not invite:
        raise HTTPException(400, detail="Invalid or already used invite")
    
    await db.users.insert_one({
        "email": email,
        "hashed_password": hash_password(req.password),
        "is_admin": False
    })
    await db.invites.update_one({"_id": invite["_id"]}, {"$set": {"used": True}})
    return {"msg": "Signup successful"}
