from fastapi import APIRouter, HTTPException
from app.schemas import Login, Token
from app.db import DB
from app.utils import verify_password, create_token

router = APIRouter(tags=["Authentication"])

@router.post("/admin/login", response_model=Token)
def login(creds: Login):
    org = DB.master().find_one({"admin_email": creds.email})
    if not org or not verify_password(creds.password, org["admin_password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_token({
        "org_name": org["name"],
        "admin_email": org["admin_email"]
    })
    return Token(access_token=token)