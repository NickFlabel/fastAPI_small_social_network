import json
from fastapi.testclient import TestClient
from social_network.app import app
from social_network.db.db import get_db, get_test_db
from social_network.db.models import Post
from social_network.tests.fixtures import database
from social_network.tests.utils import UserForTesting, PostForTesting, LikeForTesting

app.dependency_overrides[get_db] = get_test_db

db = get_test_db().__next__()

client = TestClient(app)

def test_get_likes(database):
    user = UserForTesting(db, email='test411@test.com').create_test_user()
    post = PostForTesting(user.get_user(), db=db).create_test_post()
    LikeForTesting(user=user.user, post=post.post, db=db).create_like()
    response = client.get(f'/api/posts/{post.post.id}/likes')
    assert response.status_code == 200

def test_post_like(database):
    user1 = UserForTesting(db, email='test412@test.com').create_test_user()
    user2 = UserForTesting(db, email='test413@test.com').create_test_user()
    post = PostForTesting(user1.get_user(), db=db).create_test_post()
    token = user2.login_user(client).get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post(f'/api/posts/{post.post.id}/likes', headers=headers, json={'direction': True})
    assert response.status_code == 201

def test_post_like_own_post(database):
    user = UserForTesting(db, email='test414@test.com').create_test_user()
    post = PostForTesting(user.get_user(), db=db).create_test_post()
    token = user.login_user(client).get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post(f'/api/posts/{post.post.id}/likes', headers=headers, json={'direction': True})
    assert response.status_code == 401

def test_post_already_liked_post(database):
    user1 = UserForTesting(db, email='test415@test.com').create_test_user()
    user2 = UserForTesting(db, email='test416@test.com').create_test_user()
    post = PostForTesting(user1.get_user(), db=db).create_test_post()
    LikeForTesting(user=user2.user, post=post.post, db=db).create_like()
    token = user2.login_user(client).get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post(f'/api/posts/{post.post.id}/likes', headers=headers, json={'direction': True})
    assert response.status_code == 409

def test_put_like(database):
    user1 = UserForTesting(db, email='test417@test.com').create_test_user()
    user2 = UserForTesting(db, email='test418@test.com').create_test_user()
    post = PostForTesting(user1.get_user(), db=db).create_test_post()
    LikeForTesting(user=user2.user, post=post.post, db=db).create_like()
    token = user2.login_user(client).get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.put(f'/api/posts/{post.post.id}/likes', headers=headers, json={'direction': False})
    assert response.status_code == 200
    content = json.loads(response.content)
    assert content['direction'] == False

def test_put_like_wrong_user(database):
    user1 = UserForTesting(db, email='test419@test.com').create_test_user()
    user2 = UserForTesting(db, email='test420@test.com').create_test_user()
    post = PostForTesting(user2.get_user(), db=db).create_test_post()
    LikeForTesting(user=user2.user, post=post.post, db=db).create_like()
    token = user1.login_user(client).get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.put(f'/api/posts/{post.post.id}/likes', headers=headers, json={'direction': False})
    assert response.status_code == 404

def test_delete_like(database):
    user = UserForTesting(db, email='test421@test.com').create_test_user()
    post = PostForTesting(user.get_user(), db=db).create_test_post()
    LikeForTesting(user=user.user, post=post.post, db=db).create_like()
    token = user.login_user(client).get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(f'/api/posts/{post.post.id}/likes', headers=headers)
    assert response.status_code == 204

def test_delete_like_wrong_user(database):
    user1 = UserForTesting(db, email='test422@test.com').create_test_user()
    user2 = UserForTesting(db, email='test423@test.com').create_test_user()
    post = PostForTesting(user1.get_user(), db=db).create_test_post()
    LikeForTesting(user=user2.user, post=post.post, db=db).create_like()
    token = user1.login_user(client).get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(f'/api/posts/{post.post.id}/likes', headers=headers)
    assert response.status_code == 404
