import pytest

from social_network.utils.crud import UserCrud
from social_network.tests.utils import UserForTesting
from social_network.db.db import Base, test_engine, get_test_db
from social_network.tests.fixtures import database

db = get_test_db().__next__()

class TestUserCrud:

    def test_get(self, database):
        new_user = UserForTesting(db).create_test_user()
        crud = UserCrud(db)
        assert crud.get(new_user.get_user_id(), 'id').email == new_user.get_email()

    def test_post(self, database):
        new_user = UserForTesting(db, email='test2@test.com')
        crud = UserCrud(db)
        result = crud.post(data=new_user.get_userdata())
        assert result.email == new_user.get_email()

    def test_put(self, database):
        new_user = UserForTesting(db, email='test3@test.com').create_test_user()
        crud = UserCrud(db)
        new_user.email = 'test4@test2.com'
        result = crud.put(id=new_user.get_user_id(), data=new_user.get_userdata())
        assert result.email == new_user.get_email()

    def test_delete(self, database):
        new_user = UserForTesting(db, email='test4@test.com').create_test_user()
        crud = UserCrud(db)
        assert crud.delete(new_user.get_user_id())
