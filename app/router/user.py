
from .. import models,schemas,utils
from ..database import get_db

from fastapi import FastAPI,APIRouter
from fastapi.params import Body
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List  
from ..database import get_db

router = APIRouter(
    
       
        tags=["Users"]
)


@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    
    hashed_password=utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get("/users/{id}",response_model=schemas.UserCreate)
def get_user(id:int,db:Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with given id not found")
    return user


