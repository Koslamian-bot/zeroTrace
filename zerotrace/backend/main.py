from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import json
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-anon-key")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="ZeroTrace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---
class UserCredits(BaseModel):
    user_id: str
    credits: int

class WipeRequest(BaseModel):
    device_id: str
    disk_info: dict

class CertificateSubmit(BaseModel):
    device_id: str
    cert_data: dict
    signature: str

# --- Auth Helper ---
async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    try:
        # Verify JWT with Supabase
        token = authorization.split(" ")[1]
        user = supabase.auth.get_user(token)
        return user.user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# --- Endpoints ---

@app.get("/user/credits")
async def get_credits(user=Depends(get_current_user)):
    res = supabase.table("profiles").select("credits").eq("id", user.id).single().execute()
    return {"credits": res.data.get("credits", 0) if res.data else 0}

@app.post("/wipe/validate")
async def validate_wipe(req: WipeRequest, user=Depends(get_current_user)):
    # Check if user has enough credits
    res = supabase.table("profiles").select("credits").eq("id", user.id).single().execute()
    credits = res.data.get("credits", 0) if res.data else 0
    
    if credits <= 0:
        raise HTTPException(status_code=403, detail="Insufficient credits")
    
    return {"status": "authorized", "remaining_credits": credits}

@app.post("/wipe/submit")
async def submit_wipe(cert: CertificateSubmit, user=Depends(get_current_user)):
    # 1. Deduct credit
    res = supabase.table("profiles").select("credits").eq("id", user.id).single().execute()
    new_credits = (res.data.get("credits", 0) if res.data else 0) - 1
    supabase.table("profiles").update({"credits": new_credits}).eq("id", user.id).execute()
    
    # 2. Log to blockchain (simulated)
    # In production, this would call our blockchain module
    log_entry = {
        "user_id": user.id,
        "device_id": cert.device_id,
        "timestamp": datetime.utcnow().isoformat(),
        "signature": cert.signature
    }
    
    # 3. Save certificate info to DB
    supabase.table("certificates").insert({
        "user_id": user.id,
        "device_id": cert.device_id,
        "cert_data": cert.cert_data,
        "created_at": datetime.utcnow().isoformat()
    }).execute()
    
    return {"status": "success", "remaining_credits": new_credits}

@app.get("/admin/users")
async def admin_get_users(user=Depends(get_current_user)):
    # Simple admin check (e.g. email domain or a role field in profiles)
    if not user.email.endswith("@zerotrace.com"): # Dummy check
         raise HTTPException(status_code=403, detail="Admin only")
    
    res = supabase.table("profiles").select("*").execute()
    return res.data

@app.get("/admin/logs")
async def admin_get_logs(user=Depends(get_current_user)):
    if not user.email.endswith("@zerotrace.com"):
         raise HTTPException(status_code=403, detail="Admin only")
    
    res = supabase.table("certificates").select("*").execute()
    return res.data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
