from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from ..database import SessionLocal
from ..models import Users
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(min_length=3)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_user(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    return user_model

@router.put("/password/{updated_password}", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user:user_dependency, db:db_dependency, password_update:UserPasswordUpdate):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(password_update.current_password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect Password Entered!')
    user_model.hashed_password = bcrypt_context.hash(password_update.new_password)
    db.add(user_model)
    db.commit()

@router.put("/phone/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user:user_dependency, db: db_dependency, phone_number:str = Path(min_length=10, max_length=10)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed!')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()

