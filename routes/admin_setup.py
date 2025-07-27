from fastapi import APIRouter, HTTPException
from db import db
from core.security import hash_password

router = APIRouter()

@router.post("/create-admin")
async def create_admin():
    print("Hello STARTED")
    existing_admin = await db.users.find_one({"email": "admin@zentry.com"})
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin already exists")
    
    print(existing_admin)

    admin_user = {
        "email": "admin@zentry.com",
        "hashed_password": hash_password("admin123"),
        "is_admin": True,
        "is_verified": True,
    }
    await db.users.insert_one(admin_user)
    return {"message": "Admin created successfully"}
