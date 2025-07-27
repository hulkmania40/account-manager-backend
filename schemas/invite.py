from pydantic import BaseModel, EmailStr

class InviteRequest(BaseModel):
    email: EmailStr
