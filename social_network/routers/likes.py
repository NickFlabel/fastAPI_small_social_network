from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List

from social_network.db.db import get_db
from social_network.db.models import User
from social_network.utils.auth import get_current_user
from social_network.utils.crud import LikesCrud, PostCrud
from social_network import schemas

router = APIRouter(
    prefix='/api/posts',
    tags=['Likes']
)

@router.get('/{post_id}/likes', response_model=schemas.NumberOfLikes)
def get_likes(post_id: int, db: Session = Depends(get_db)):
    likes = LikesCrud(db).get(post_id, 'post_id', 'all')
    number_of_likes = 0
    for like in likes:
        if like.direction:
            number_of_likes += 1
        else:
            number_of_likes -= 1
    return {'number_of_likes': number_of_likes}

@router.post('/{post_id}/likes', response_model=schemas.Like, status_code=201)
def post_like(post_id: int, direction: schemas.LikePost, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = PostCrud(db).get(post_id, 'id')
    if not post:
        raise HTTPException(status_code=404)
    elif post.user_id == user.id:
        raise HTTPException(status_code=401)
    elif LikesCrud(db).user_vote_on_post(post.id, user.id):
        raise HTTPException(status_code=409)
    else:
        like_data = schemas.Like(user_id=user.id, post_id=post.id, direction=direction.direction)
        new_vote = LikesCrud(db).post(like_data)
        return new_vote

@router.put('/{post_id}/likes', response_model=schemas.Like, status_code=200)
def put_like(post_id: int, direction: schemas.LikePost, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = PostCrud(db).get(post_id, 'id')
    if not post:
        raise HTTPException(status_code=404)
    else:
        like = LikesCrud(db).user_vote_on_post(post.id, user.id)
        if not like:
            raise HTTPException(status_code=404)
        like_data = schemas.Like(user_id=user.id, post_id=post.id, direction=direction.direction)
        new_vote = LikesCrud(db).put(id=like.id, data=like_data)
        return new_vote
    
@router.delete('/{post_id}/likes', status_code=204)
def put_like(post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = PostCrud(db).get(post_id, 'id')
    if not post:
        raise HTTPException(status_code=404)
    else:
        like = LikesCrud(db).user_vote_on_post(post.id, user.id)
        if not like:
            raise HTTPException(status_code=404)
        new_vote = LikesCrud(db).delete(id=like.id)
        return new_vote