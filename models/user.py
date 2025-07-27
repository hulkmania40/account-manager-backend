from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

class User(BaseModel):
    email: EmailStr
    hashed_password: str
    is_admin: bool = False
