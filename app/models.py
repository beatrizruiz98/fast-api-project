from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel


class Posts(SQLModel, table=True):
    """Tabla principal para almacenar el contenido que crean los usuarios."""

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Uso SQLAlchemy para definir la clave foránea con ondelete="CASCADE" (no disponible en SQLModel).
    user_id: int = Field(sa_column=Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False))

    # Relación inversa para recuperar el autor del post de forma directa.
    user: "Users" = Relationship(back_populates="post")


class Users(SQLModel, table=True):
    """Información básica de cada usuario registrado y autenticado."""

    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    phone_number: str = Field(nullable=True)

    # Relación inversa: lista de posts creados por el usuario.
    post: list[Posts] = Relationship(back_populates="user")


class Votes(SQLModel, table=True):
    """Tabla intermedia que relaciona usuarios con posts votados."""

    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    )
    post_id: int = Field(
        sa_column=Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    )
