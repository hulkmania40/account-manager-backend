from pydantic import BaseModel, EmailStr
from datetime import datetime

class Invite(BaseModel):
    email: EmailStr
    token: str
    created_at: datetime
    used: bool = False
