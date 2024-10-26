from fastapi import FastAPI, HTTPException, Path
from app import crud, schemas
from app.database import engine, Base, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List


app = FastAPI()

# Создание базы данных
Base.metadata.create_all(bind=engine)


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found with the given query")
    return posts


@app.get("/posts/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.post("/posts", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post)


@app.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    db_post = crud.update_post(db, post_id=post_id, post=post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.delete("/posts/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.delete_post(db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.get("/posts/search/{query}", response_model=List[schemas.Post])
def search_posts(query: str, db: Session = Depends(get_db)):
    posts = crud.search_posts(db, query=query)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found with the given query")
    return posts


@app.get("/posts/statistics/{user_id}")
def get_user_post_statistics(user_id: int = Path(...), db: Session = Depends(get_db)):
    avg_posts_per_month = crud.calculate_avg_posts_per_month(db, user_id=user_id)
    if not avg_posts_per_month:
        raise HTTPException(status_code=404, detail="No posts found with the given query")
    return {"user_id": user_id, "average_posts_per_month": avg_posts_per_month}
