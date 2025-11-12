from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from ..database import get_session
from ..models import Users
from ..oauth2 import create_access_token
from ..schemas import Token
from ..utils import verify

# Router encargado de la autenticación basada en username/password -> JWT.
router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=Token)
def login_user(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    """Valida credenciales recibidas vía formulario OAuth2 y emite un token JWT."""
    # OAuth2PasswordRequestForm tiene "username" y "password", no email, tenemos que modificarlo aunque username = email usuario a efectos prácticos
    # Esta request se hace desde form-data
    user = db.exec(select(Users).where(Users.email == payload.username)).first()
    # Si no existe el usuario
    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    # Verificar la contraseña
    if verify(payload.password, user.password) is False:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    else:
        access_token = create_access_token(data={"user_id": user.id})
        return {"access_token": access_token}
