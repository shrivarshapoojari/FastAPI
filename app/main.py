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

 

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}
    



@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))

    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    return {"post_detail": post}

  
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):

    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)  RETURNING *""",(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
     
   
    return {"data":new_post}







@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    return {"data": updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()



 
    if deleted_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
     
    return {"message": "Post deleted successfully"}