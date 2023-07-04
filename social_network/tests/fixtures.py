import pytest
import json
from sqlalchemy.orm import sessionmaker
from social_network.app import app
from social_network.db.db import Base, test_engine, SessionTest


@pytest.fixture(scope='module')
def database():
    SessionTest.close_all()
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield

    