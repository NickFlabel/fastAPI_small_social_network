from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List

from social_network.db.db import get_db
from social_network.db.models import User
from social_network.utils.auth import get_current_user
from social_network.utils.crud import PostCrud
from social_network import schemas

router = APIRouter(
    prefix='/api',
    tags=['Posts']
)

@router.get('/posts', response_model=List[schemas.Post])
def get_all_posts(db: Session = Depends(get_db)):
    return PostCrud(db).get()

@router.get('/posts/{post_id}', response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = PostCrud(db).get(post_id, 'id')
    if post:
        return post
    else:
        raise HTTPException(status_code=404)
    
@router.post('/posts', response_model=schemas.Post, status_code=201)
def post_a_post(data: schemas.PostCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data.user_id = user.id
    post = PostCrud(db).post(data=data)
    return post

@router.put('/posts/{post_id}', response_model=schemas.Post)
def put(post_id: int, data: schemas.PostCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post_crud = PostCrud(db)
    post = post_crud.get(post_id, 'id')
    if not post:
        raise HTTPException(status_code=404)
    if post.user_id != user.id:
        raise HTTPException(status_code=401)
    data.user_id = user.id
    post = PostCrud(db).put(data=data, id=post_id)
    return post

@router.delete('/posts/{post_id}', status_code=204)
def delete(post_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post_crud = PostCrud(db)
    post = post_crud.get(post_id, 'id')
    if not post:
        raise HTTPException(status_code=404)
    if post.user_id != user.id:
        raise HTTPException(status_code=401)
    post = PostCrud(db).delete(post_id)
