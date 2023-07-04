from sqlalchemy.orm import Session
from social_network.db import models
from social_network import schemas
from social_network.db.db import get_test_db
from social_network.utils.auth import hash
from typing import Optional
import json


class UserForTesting:

    def __init__(self, db: Optional[Session] = None, 
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 email: Optional[str] = None) -> None:
        self.user = None
        self.username = username if username else 'test'
        self.password = password if password else 'test'
        self.email = email if email else 'test@test.com'
        if not db:
            self.db = get_test_db().__next__()
        else:
            self.db = db

    def create_test_user(self):
        user = schemas.UserRegistration(username=self.username, email=self.email, password=self.password)
        user.password = hash(self.password)
        db_user = models.User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        self.user = db_user
        return self
    
    def login_user(self, client):
        if not self.user:
            return False
        response = client.post('/api/login', json={'email': self.get_email(), 'password': self.password})
        self.token = json.loads(response.content)['access_token']
        return self
    
    def get_token(self):
        return self.token
    
    def get_userdata(self):
        return schemas.UserRegistration(username=self.username, email=self.email, password=self.password)
    
    def get_user(self):
        return self.user
    
    def get_user_id(self):
        return self.user.id
    
    def get_email(self):
        return self.email
    
    def get_username(self):
        return self.username
    

class PostForTesting:

    def __init__(self, 
                 user: models.User, 
                 db: Optional[Session] = None,
                 content: Optional[str] = None 
                 ) -> None:
        self.user = user
        self.content = content if content else 'test'
        if not db:
            self.db = get_test_db().__next__()
        else:
            self.db = db
    
    def create_test_post(self):
        post = schemas.PostCreate(content=self.content)
        db_post = models.Post(**post.dict())
        db_post.user_id = self.user.id
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        self.post = db_post
        return self
    

class LikeForTesting:
        
    def __init__(self, 
                 user: models.User, 
                 post: models.Post,
                 db: Optional[Session] = None,
                 direction: bool = True
                 ) -> None:
        self.user = user
        self.post = post
        self.direction = direction
        if not db:
            self.db = get_test_db().__next__()
        else:
            self.db = db

    def create_like(self):
        like = schemas.Like(user_id=self.user.id, post_id=self.post.id, direction=self.direction)
        db_like = models.Like(**like.dict())
        self.db.add(db_like)
        self.db.commit()
        self.db.refresh(db_like)
        self.like = db_like
        return self
