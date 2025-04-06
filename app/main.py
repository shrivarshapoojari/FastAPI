from  fastapi import FastAPI
from fastapi.params import Body
from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras  import RealDictCursor
import time
app = FastAPI()




class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[float] = None


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="root", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("PostgreSQL connection is open")
        break
    except Exception as e:
        print("Error while connecting to PostgreSQL:", e)
        time.sleep(2)

 
 




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

  
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    print(post)
    print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data":my_posts[-1]}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = 0
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            index = i
            break
    if index == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    
    my_posts.pop(index)
    return {"message": "Post deleted successfully"}