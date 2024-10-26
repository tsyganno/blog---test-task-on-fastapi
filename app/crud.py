from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy import func, extract
from datetime import datetime


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: int, post: schemas.PostUpdate):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        if post.title is not None:
            db_post.title = post.title
        if post.content is not None:
            db_post.content = post.content
        db_post.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post


def search_posts(db: Session, query: str):
    return db.query(models.Post).filter((models.Post.title.contains(query)) | (models.Post.content.contains(query))).all()


def calculate_avg_posts_per_month(db: Session, user_id: int):
    current_year = datetime.now().year

    # Подсчет количества постов, созданных каждым месяцем в текущем году
    monthly_posts = (db.query(extract('month', models.Post.created_at).label("month"), func.count(models.Post.id)).filter(models.Post.user_id == user_id).filter(extract('year', models.Post.created_at) == current_year).group_by(extract('month', models.Post.created_at)).all())

    # Подсчет среднего количества постов в месяц
    total_posts = sum(count for month, count in monthly_posts)
    num_months = len(monthly_posts)
    avg_posts_per_month = total_posts / num_months if num_months > 0 else 0

    return avg_posts_per_month
