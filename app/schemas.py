from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

from pydantic import conint

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None
  




class PostCreate(PostBase):
    pass



class Post(PostBase):
    id: int
   
    created_at: datetime

    owner_id: int
    owner:UserOut

     
    

    class Config:
        orm_mode = True




class UserCreate(BaseModel):
    email: EmailStr
    password: str







class UserLogin(BaseModel):
    email: EmailStr
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    id:Optional[str] = None
    



class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    