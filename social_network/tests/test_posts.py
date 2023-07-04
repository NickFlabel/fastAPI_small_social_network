import json
from fastapi.testclient import TestClient
from social_network.app import app
from social_network.db.db import get_db, get_test_db
from social_network.db.models import Post
from social_network.tests.fixtures import database
from social_network.tests.utils import UserForTesting, PostForTesting

app.dependency_overrides[get_db] = get_test_db

db = get_test_db().__next__()

client = TestClient(app)

def test_get_all_posts(database):
    user = UserForTesting(db).create_test_user()
    post = PostForTesting(user.get_user()).create_test_post()
    response = client.get('/api/posts')
    assert response.status_code == 200
    content = json.loads(response.content)
    assert content[0]['content'] == post.content

def test_one_post(database):
    user = UserForTesting(db, email='test311@test.com').create_test_user()
    post = PostForTesting(user.get_user()).create_test_post()
    response = client.get(f'/api/posts/{post.post.id}')
    assert response.status_code == 200

def test_invalid_post_id(database):
    response = client.get(f'/api/posts/1234567')
    assert response.status_code == 404

def test_post(database):
    user = UserForTesting(db, email='test312@test.com').create_test_user()
    content = 'test'
    token = user.login_user(client).get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post('/api/posts', headers=headers, json={'content': content})
    assert response.status_code == 201
    content = json.loads(response.content)
    id = content['id']
    new_post = db.query(Post).filter(Post.id==id).first()
    assert new_post.user == user.user
    assert new_post.user.id == user.user.id

def test_put(database):
    user = UserForTesting(db, email='test313@test.com').create_test_user()
    post = PostForTesting(user.get_user()).create_test_post()
    new_content = 'new_test'
    token = user.login_user(client).get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.put(f'/api/posts/{post.post.id}', headers=headers, json={'content': new_content})
    assert response.status_code == 200

def test_put_wrong_user(database):
    user1 = UserForTesting(db, email='test314@test.com').create_test_user()
    user2 = UserForTesting(db, email='test315@test.com').create_test_user()
    post = PostForTesting(user1.get_user()).create_test_post()
    new_content = 'new_test'
    token = user2.login_user(client).get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.put(f'/api/posts/{post.post.id}', headers=headers, json={'content': new_content})
    assert response.status_code == 401

def test_delete(database):
    user = UserForTesting(db, email='test316@test.com').create_test_user()
    post = PostForTesting(user.get_user()).create_test_post()
    new_content = 'new_test'
    token = user.login_user(client).get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(f'/api/posts/{post.post.id}', headers=headers)
    assert response.status_code == 204

def test_delete_wrong_user(database):
    user1 = UserForTesting(db, email='test317@test.com').create_test_user()
    user2 = UserForTesting(db, email='test318@test.com').create_test_user()
    post = PostForTesting(user1.get_user()).create_test_post()
    token = user2.login_user(client).get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(f'/api/posts/{post.post.id}', headers=headers)
    assert response.status_code == 401
