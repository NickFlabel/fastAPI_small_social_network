from abc import ABC, abstractmethod
from typing import Optional, Any
from social_network.schemas import UserRegistration
from sqlalchemy.orm import Session
from social_network.db import models

class Crud(ABC):
    model = None

    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, value: Optional[Any] = None, field_name: Optional[str] = None, scope: str = 'first'):
        if not field_name and not value:
            return self.db.query(self.model).all()
        if hasattr(self.model, field_name):
            query = self.db.query(self.model)
            filter_condition = getattr(self.model, field_name) == value
            if scope == 'first':
                entity = query.filter(filter_condition).first()
            elif scope == 'all':
                entity = query.filter(filter_condition).all()
        else:
            raise ValueError('Value not found')
        return entity

    def post(self, data):
        db_entity = self.model(**data.dict())
        self.db.add(db_entity)
        self.db.commit()
        self.db.refresh(db_entity)
        return db_entity

    def put(self, id, data):
        db_entity = self.get(id, 'id')
        for key, value in data.dict().items():
            if hasattr(db_entity, key):
                setattr(db_entity, key, value)
        self.db.commit()
        self.db.refresh(db_entity)
        return db_entity

    def delete(self, id):
        db_entity = self.get(id, 'id')
        if not db_entity:
            return False
        self.db.delete(db_entity)
        self.db.commit()
        return True


class UserCrud(Crud):
    model = models.User


class PostCrud(Crud):
    model = models.Post


class LikesCrud(Crud):
    model = models.Like

    def user_vote_on_post(self, post_id, current_user_id):
        vote_query = self.db.query(self.model).filter(self.model.post_id == post_id, self.model.user_id == current_user_id)
        return vote_query.first() 