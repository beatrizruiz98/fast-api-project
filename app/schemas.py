from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    created_at: Optional[datetime] = None

class UserIn(UserBase):
    password: str
    phone_number: Optional[str] = None

class UserOut(UserBase):
    phone_number: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)  # 1 for upvote, 0 for remove vote

class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    
class PostCreate(PostBase):
    created_at: Optional[datetime] = None
    id: Optional[int] = None

class PostOut(PostBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    user: UserBase = None

class PostsWithVotes(BaseModel):
    Posts: PostOut
    votes: int 

class Token(BaseModel):
    token_type: str = "Bearer"
    access_token: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    

