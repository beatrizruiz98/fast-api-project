from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Users
from ..schemas import UserLogin
from ..utils import verify

router = APIRouter(tags=["Authentication"])

@router.post("/login", status_code=status.HTTP_201_CREATED)
def login_user(payload: UserLogin, db: Session = Depends(get_session)):
    user = db.exec(select(Users).where(Users.email == payload.email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if verify(payload.password, user.password) == False:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        return {"message": "Login successful"}