from fastapi import FastAPI
from routes import admin_setup, auth, invite
from slowapi import Limiter
from slowapi.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(invite.router, prefix="/invite", tags=["invite"])
app.include_router(admin_setup.router)

@app.get("/")
def read_root():
    return {"message": "API is running"}

# uvicorn main:app --reload
