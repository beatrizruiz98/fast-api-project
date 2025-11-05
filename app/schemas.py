from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    
class PostIn(PostBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
class UserBase(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    created_at: Optional[datetime] = None

class UserIn(UserBase):
    password: str

