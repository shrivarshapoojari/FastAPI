from  fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
app = FastAPI()




class Post(BaseModel):
    title: str
    content: str
     

@app.get("/")
def read_root():
    return {  "World1"}


@app.post("/posts")
def create_post(post: Post):
    return {"post": post['title']}