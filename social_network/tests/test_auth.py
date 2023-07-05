import pytest
import json
from fastapi.testclient import TestClient
from social_network.app import app
from social_network.db.db import Base, test_engine, get_db, get_test_db
from social_network.utils.crud import UserCrud
from social_network.db.models import User
from social_network.tests.fixtures import database
from social_network.tests.utils import UserForTesting
from social_network.utils.auth import get_current_user
from social_network.config import Settings, get_settings

def get_test_settings():
    settings = Settings()
    settings.email_validation = False
    return settings

app.dependency_overrides[get_db] = get_test_db
app.dependency_overrides[get_settings] = get_test_settings

db = get_test_db().__next__()

client = TestClient(app)

@pytest.fixture
def userdata():
    return {
        'email': 'test@test.com',
        'username': 'test',
        'password': 'test'
    }


def test_registration(userdata, database):
    response = client.post('/api/register', json=userdata)
    assert response.status_code == 200
    assert UserCrud(db=db).get(value=userdata['email'], field_name='email') is not None 

def test_registration_invalid_data(userdata, database):
    invalid_data = userdata
    del invalid_data['password']
    response = client.post('/api/register', json=userdata)
    assert response.status_code == 422

def test_registration_already_exists(userdata, database):
    response = client.post('/api/register', json=userdata)
    assert response.status_code == 400

def test_password_hashing(userdata, database):
    userdata['email'] = 'test2@test.com'
    response = client.post('/api/register', json=userdata)
    content = json.loads(response.content)
    id = content['id']
    user = db.query(User).filter(User.id == id).first()
    assert userdata['password'] != user.password

def test_login(userdata, database):
    user = UserForTesting(db, email='test54@test.com').create_test_user()
    response = client.post('/api/login', json={'email': user.get_email(), 'password': user.password})
    assert response.status_code == 200
    jwt_token = json.loads(response.content)['access_token']
    assert user.user == get_current_user(jwt_token, db)

def test_login_invalid_credentials(userdata, database):
    user = UserForTesting(db, email='test99@test.com')
    response = client.post('/api/login', json={'email': user.get_email(), 'password': user.password})
    assert response.status_code == 403
