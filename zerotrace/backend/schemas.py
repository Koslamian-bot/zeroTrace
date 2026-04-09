from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    wipes_remaining: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class WipeLogBase(BaseModel):
    device_id: str
    status: str

class WipeLogCreate(WipeLogBase):
    pass

class WipeLogResponse(WipeLogBase):
    id: str
    user_id: str
    timestamp: datetime

    class Config:
        from_attributes = True

class CertificateBase(BaseModel):
    device_info: str
    hash: str

class CertificateCreate(CertificateBase):
    pass

class CertificateResponse(CertificateBase):
    id: str
    user_id: str
    timestamp: datetime

    class Config:
        from_attributes = True
