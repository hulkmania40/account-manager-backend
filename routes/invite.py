from fastapi import APIRouter, HTTPException, Depends
from schemas.invite import InviteRequest
from core.security import create_token
from services.email import send_invite_email
from middleware.auth import require_admin
from datetime import timedelta, datetime
from db import db
from core.config import settings

router = APIRouter()

@router.post("/")
async def send_invite(req: InviteRequest, admin=Depends(require_admin)):
    existing = await db.users.find_one({"email": req.email})
    if existing:
        raise HTTPException(400, detail="User already exists")
    
    token_data = {"sub": req.email}
    token = create_token(token_data, timedelta(minutes=settings.INVITE_TOKEN_EXPIRE_MINUTES), "invite")
    
    await db.invites.insert_one({
        "email": req.email,
        "token": token,
        "created_at": datetime.utcnow(),
        "used": False
    })
    
    await send_invite_email(req.email, token)
    return {"msg": "Invite sent"}
