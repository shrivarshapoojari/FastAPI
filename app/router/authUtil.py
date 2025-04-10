from jose import JWTError,jwt
from datetime import datetime, timedelta
from fastapi import HTTPException,status,   Depends
from fastapi.security import OAuth2PasswordBearer
from .. import schemas, database,models
from fastapi import Depends
from sqlalchemy.orm import Session

SECRET_KEY="anfdvndkvnfdkvjdkvm;s;vmdvkdmvdlvvdv;d"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=300000


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt



def verify_access_token(token:str):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id=payload.get("user_id")
        if id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    token_data=schemas.TokenData(id=str(id))
    return token_data



def get_current_user(token:str =Depends(oauth2_scheme),db:Session=Depends(database.get_db)):

    token=verify_access_token(token=token)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    return user
     
   

