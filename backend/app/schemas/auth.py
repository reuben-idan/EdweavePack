from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str
    institution: Optional[str] = None
    role: str = "teacher"

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    full_name: Optional[str] = None
    is_active: bool
    institution: Optional[str] = None
    role: Optional[str] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    password: str

class UpdateProfileRequest(BaseModel):
    fullName: str
    email: str
    institution: str

class UpdatePasswordRequest(BaseModel):
    current_password: str
    new_password: str