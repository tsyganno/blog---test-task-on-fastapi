from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import List


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    user_id: int


# Новая схема для обновления
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    posts: List[Post] = []

    class Config:
        orm_mode = True
