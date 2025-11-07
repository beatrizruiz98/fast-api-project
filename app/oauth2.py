import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta, timezone

from .schemas import TokenData
from .database import get_session
from .models import Users

from sqlmodel import Session, select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # Refering login endpoint

SECRET_KEY = "6e3eebaad224dab29d0cfefde1622bfc338f4e3518ab4faa9c19d02307fc4a62" # Generate by openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None): # Time expiration can be added manually
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=str(id))
        
    except InvalidTokenError:
        raise credentials_exception
    
    return token_data

# Si envio una petición sin Authorization header en aquellos endpoints que tienen un Depends en get_current_user 
# lanza un 401 "detail": "Not authenticated" generado de manera automática por FastAPI de la funcion OAuth2PasswordBearer
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
   
   # Esto devuelve el token data (user id) definido en verify_user o lanza excepción) 
    token = verify_access_token(token, credentials_exception) 
    # Se usa token.id por el schema TokenData
    user = db.exec(select(Users).where(Users.id == token.id)).first()
    
    return user.id
