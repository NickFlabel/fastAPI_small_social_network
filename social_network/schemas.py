from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from social_network.db.models import User, Post


class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str

    class Config:
        orm_mode = True

class UserLoginData(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class Post(BaseModel):
    id: int
    content: str
    user_id: int

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    content: str
    user_id: Optional[int]

    class Config:
        orm_mode = True

class Like(BaseModel):
    user_id: int
    post_id: int
    direction: bool

    class Config:
        orm_mode = True

class LikePost(BaseModel):
    direction: bool

class NumberOfLikes(BaseModel):
    number_of_likes: int
