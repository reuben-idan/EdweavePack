from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    institution: str = None
    role: str = "teacher"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    institution: str = None
    role: str = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str