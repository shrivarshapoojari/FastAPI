from fastapi import FastAPI
from fastapi.params import Body
from fastapi import HTTPException, status
from .schemas import PostCreate
from . import schemas
from random import randrange
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List  
from . import utils
from  .router import post, user,auth
models.Base.metadata.create_all(bind=engine)

app = FastAPI()




app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

