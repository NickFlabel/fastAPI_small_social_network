from sqlalchemy import ForeignKey, String, Integer, DateTime, BigInteger, Text
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql import func
from typing import Optional, List
from datetime import datetime

from social_network.db.db import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    posts: Mapped[List['Post']] = relationship(back_populates='user', cascade='all, delete-orphan')
    likes: Mapped[List['Like']] = relationship(back_populates='user', cascade='all, delete-orphan')


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='posts')
    likes: Mapped[List['Like']] = relationship(back_populates='post', cascade='all, delete-orphan')


class Like(Base):
    __tablename__ = 'likes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='likes')
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    post: Mapped['Post'] = relationship('Post', back_populates='likes')
    direction: Mapped[bool]
