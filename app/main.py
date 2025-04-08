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
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


 

@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts





@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post



@app.post("/posts", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return   post_query.first()





@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.PostCreate).filter(models.PostCreate.id == id)
    deleted_post = post_query.first()
    if deleted_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post deleted successfully"}
