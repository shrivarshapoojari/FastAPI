
from .. import models,schemas,utils
from ..database import get_db

from fastapi import FastAPI,APIRouter
from fastapi.params import Body
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List  
from ..database import get_db

from  . import authUtil

from ..schemas import PostCreate

router = APIRouter(

    tags=["Posts"]
)

@router.get("/posts",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),
                user:int=Depends(authUtil.get_current_user),
                 limit: int = 10,
                 skip: int = 0,
                 search: str = ""
              ):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts





@router.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db),
             user:int=Depends(authUtil.get_current_user),
            
             ):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post



@router.post("/posts",
              
              status_code=status.HTTP_201_CREATED,
              response_model=schemas.Post,
 
             
             )
def create_post(post: PostCreate, 
                db: Session = Depends(get_db),
                user:int=Depends(authUtil.get_current_user),
                
                
                ):
    print(user)
 
    new_post = models.Post(**post.dict())
    new_post.owner_id=user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




@router.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)
                ,
                user:int=Depends(authUtil.get_current_user)
                ):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if updated_post.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return   post_query.first()





@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)
                ,
                user:int=Depends(authUtil.get_current_user)
                ):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    deleted_post = post_query.first()
   
    if deleted_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if deleted_post.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post deleted successfully"}


