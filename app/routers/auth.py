from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlmodel import Session, select

from ..database import get_session
from ..models import Users
from ..schemas import Token
from ..utils import verify
from ..oauth2 import create_access_token

router = APIRouter(tags=["Authentication"])

@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=Token)
def login_user(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    
    # OAuth2PasswordRequestForm tiene "username" y "password", no email, tenemos que modificarlo aunque username = email usuario a efectos prácticos
    # Esta request se hace desde form-data
    
    user = db.exec(select(Users).where(Users.email == payload.username)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if verify(payload.password, user.password) == False:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        access_token = create_access_token(data={"user_id": user.id})
        return {"access_token": access_token}