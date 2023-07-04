from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional, List
import uuid
from .. import models
from sqlalchemy.orm import Session 
from sqlalchemy.exc import IntegrityError
from ..utils.helpers import get_hash
from ..schemas import UserCreate, UserOut
from ..database import get_db



router = APIRouter(
    prefix="/users",
    tags=['Users']
)



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user:UserCreate, db:Session= Depends(get_db)):
    
    user.password = get_hash(user.password)
    new_user = models.User(**user.dict())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User Already exists with that email")



@router.get("/{id}", response_model=UserOut)
def get_user(id:int, db:Session= Depends(get_db)):


    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    else:
        return user