from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlmodel import Session, select
from ..database import get_session
from ..models import Users
from ..schemas import UserBase, UserIn
from ..utils import get_password_hash

router = APIRouter(
    prefix = "/users"
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=UserBase)
def create_user(payload: UserIn, db: Session = Depends(get_session)):
    payload.password = get_password_hash(payload.password)
    user = Users(**payload.model_dump())
    if db.exec(select(Users).where(Users.email == user.email)).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    db.add(user, id)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserBase)
def get_user(id: int, db: Session = Depends(get_session)):
    user = db.get(Users, id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {id} was not found")
    return user