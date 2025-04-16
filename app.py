from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# نموذج البيانات
class Post(BaseModel):
    id: int
    title: str
    content: str

# قاعدة بيانات وهمية في الذاكرة
posts_db: List[Post] = []

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Blog API!"}

@app.get("/posts", response_model=List[Post])
def get_posts():
    return posts_db

@app.get("/posts/{post_id}", response_model=Post)
def get_post(post_id: int):
    for post in posts_db:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

@app.post("/posts", response_model=Post)
def create_post(post: Post):
    posts_db.append(post)
    return post

@app.put("/posts/{post_id}", response_model=Post)
def update_post(post_id: int, updated_post: Post):
    for i, post in enumerate(posts_db):
        if post.id == post_id:
            posts_db[i] = updated_post
            return updated_post
    raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    for i, post in enumerate(posts_db):
        if post.id == post_id:
            del posts_db[i]
            return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")