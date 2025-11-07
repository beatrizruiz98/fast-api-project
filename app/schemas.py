from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    created_at: Optional[datetime] = None

class UserIn(UserBase):
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    
class PostCreate(PostBase):
    created_at: Optional[datetime] = None
    id: Optional[int] = None
    pass

class PostOut(PostBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    user: UserBase = None

class Token(BaseModel):
    token_type: str = "Bearer"
    access_token: str
    
class TokenData(BaseModel):
    id: Optional[str] = None

