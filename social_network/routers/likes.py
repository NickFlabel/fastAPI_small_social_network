from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List

from social_network.db.db import get_db
from social_network.db.models import User
from social_network.utils.auth import get_current_user
from social_network.utils.crud import LikesCrud, PostCrud
from social_network import schemas
from social_network.redis import redis_client
from social_network.config import get_settings

router = APIRouter(
    prefix='/api/posts',
    tags=['Likes']
)

@router.get('/{post_id}/likes', response_model=schemas.NumberOfLikes)
def get_likes(post_id: int, db: Session = Depends(get_db), settings = Depends(get_settings)):
    post = PostCrud(db).get(post_id, 'id')
    if not post:
        raise HTTPException(status_code=404)
    cached_likes = redis_client.get(f'likes:{post_id}')
    if cached_likes and settings.caching:
        number_of_likes = int(cached_likes)
    else:
        likes = LikesCrud(db).get(post_id, 'post_id', 'all')
        number_of_likes = 0
        for like in likes:
            if like.direction:
                number_of_likes += 1
            else:
                number_of_likes -= 1
        if settings.caching: 
            redis_client.set(f'likes:{post_id}', number_of_likes)
    return {'number_of_likes': number_of_likes}

@router.post('/{post_id}/likes', response_model=schemas.Like, status_code=201)
def post_like(post_id: int, direction: schemas.LikePost, db: Session = Depends(get_db), user: User = Depends(get_current_user), settings = Depends(get_settings)):
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
        cache_key = f'likes:{post_id}'
        if settings.caching:
            cached_likes = redis_client.get(cache_key)
            if cached_likes:
                current_likes = int(cached_likes)
                if bool(direction.direction):
                    current_likes += 1
                else:
                    current_likes -= 1
                redis_client.set(cache_key, current_likes)
        return new_vote

@router.put('/{post_id}/likes', response_model=schemas.Like, status_code=200)
def put_like(post_id: int, direction: schemas.LikePost, db: Session = Depends(get_db), user: User = Depends(get_current_user), settings = Depends(get_settings)):
    post = PostCrud(db).get(post_id, 'id')
    if not post:
        raise HTTPException(status_code=404)
    else:
        like = LikesCrud(db).user_vote_on_post(post.id, user.id)
        if not like:
            raise HTTPException(status_code=404)
        old_direction = like.direction
        like_data = schemas.Like(user_id=user.id, post_id=post.id, direction=bool(direction.direction))
        new_vote = LikesCrud(db).put(id=like.id, data=like_data)
        cache_key = f'likes:{post_id}'
        if settings.caching:
            cached_likes = redis_client.get(cache_key)
            if cached_likes:
                current_likes = int(cached_likes)
                if direction.direction:
                    if not old_direction:
                        current_likes += 2
                else:
                    if old_direction:
                        current_likes -= 2
                redis_client.set(cache_key, current_likes)
        return new_vote
    
@router.delete('/{post_id}/likes', status_code=204)
def put_like(post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user), settings = Depends(get_settings)):
    post = PostCrud(db).get(post_id, 'id')
    if not post:
        raise HTTPException(status_code=404)
    else:
        like = LikesCrud(db).user_vote_on_post(post.id, user.id)
        if not like:
            raise HTTPException(status_code=404)
        LikesCrud(db).delete(id=like.id)
        if settings.caching:
            cache_key = f'likes:{post_id}'
            cached_likes = redis_client.get(cache_key)
            if cached_likes:
                current_likes = int(cached_likes)
                if bool(like.direction):
                    current_likes -= 1
                else:
                    current_likes += 1
                redis_client.set(cache_key, current_likes)
        return 