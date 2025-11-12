from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


class UserBase(BaseModel):
    """Campos comunes compartidos por varias respuestas relacionadas con usuarios."""

    id: Optional[int] = None
    email: EmailStr
    created_at: Optional[datetime] = None


class UserIn(UserBase):
    """Payload esperado cuando se crea un usuario a través de la API."""

    password: str
    phone_number: Optional[str] = None


class UserOut(UserBase):
    """Información pública que se expone al consultar un usuario."""

    phone_number: Optional[str] = None


class Vote(BaseModel):
    """Modelo para indicar si se crea o elimina un voto sobre un post."""

    post_id: int
    dir: conint(ge=0, le=1)  # 1 for upvote, 0 for remove vote


class PostBase(BaseModel):
    """Campos básicos que definen el contenido de un post."""

    title: str
    content: str
    published: Optional[bool] = True


class PostCreate(PostBase):
    """Respuesta tras crear un post, incluyendo metadata adicional."""

    created_at: Optional[datetime] = None
    id: Optional[int] = None


class PostOut(PostBase):
    """Post que se devuelve en consultas, enriquecido con información del autor."""

    id: Optional[int] = None
    created_at: Optional[datetime] = None
    user: UserBase = None


class PostsWithVotes(BaseModel):
    """Estructura combinada para devolver post + recuento de votos."""

    Posts: PostOut
    votes: int


class Token(BaseModel):
    """Representa el token JWT emitido al autenticarse."""

    token_type: str = "Bearer"
    access_token: str


class TokenData(BaseModel):
    """Datos mínimos almacenados dentro del JWT (por ahora sólo el user_id)."""

    id: Optional[str] = None
