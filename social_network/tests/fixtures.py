import pytest
from social_network.app import app
from social_network.db.db import Base, test_engine, SessionTest
from social_network.config import Settings, get_settings
from social_network.db.db import Base, test_engine, get_db, get_test_db

def get_test_settings():
    settings = Settings()
    settings.email_validation = False
    settings.caching = False
    return settings

@pytest.fixture
def override_db_and_settings():
    app.dependency_overrides[get_db] = get_test_db
    app.dependency_overrides[get_settings] = get_test_settings

@pytest.fixture(scope='module')
def database():
    SessionTest.close_all()
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield

    