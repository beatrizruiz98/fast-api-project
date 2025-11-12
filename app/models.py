from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, ForeignKey, Integer
from datetime import datetime
from pydantic import EmailStr

class Posts(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool  = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Uso sqlalchemy para definir la clave foránea con ondelete="CASCADE" (No disponible en SQLMOdel)
    user_id: int = Field(sa_column=Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"),nullable=False))
    
    # Devuelve el usuario asociado a este post (usado para devolver el autor del post)
    user: "Users" = Relationship(back_populates="post")
     
class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    phone_number: str = Field(nullable=True)
    
    # Devuelve los posts asociados a este usuario (necesario para la relación inversa)
    post: list[Posts] = Relationship(back_populates="user")

class Votes(SQLModel, table=True):
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    )
    post_id: int = Field(
        sa_column=Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    )