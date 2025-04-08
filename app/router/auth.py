from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils  
from . import authUtil
router = APIRouter( 
    tags=["Auth"],
    prefix="/auth"
)


@router.post("/login")
def login(user_credentials:schemas.UserLogin ,  db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    acess_token= authUtil.create_access_token(data={"user_id":user.id})
    return {"access_token":acess_token, "token_type":"bearer"}
    


