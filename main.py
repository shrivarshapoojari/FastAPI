from  fastapi import FastAPI
from fastapi.params import Body
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()




class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[float] = None


my_posts = [
    {"id": 1, "title": "First post", "content": "Hello world!", "published": True, "rating": 4.5},
    {"id": 2, "title": "Second post", "content": "FastAPI is awesome!", "published": False}
]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
    return None

@app.get("/posts")
def get_posts():
    return { "data": my_posts }



@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    return {"post_detail": post}

  
@app.post("/posts")
def create_post(post: Post):
    print(post)
    print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data":my_posts[-1]}