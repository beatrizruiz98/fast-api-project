from sqlmodel import Field, SQLModel
from datetime import datetime
from pydantic import EmailStr

class Posts(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool  = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)