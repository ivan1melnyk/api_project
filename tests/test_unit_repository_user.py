import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.repository.user import (
    get_user_by_email, create_user, update_token
)

from src.database.models import User
import unittest
from unittest.mock import MagicMock
from src.schemas import UserModel
from sqlalchemy.orm import Session


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, email='any.adress11@gmail.com')

    async def test_get_user_by_email(self):
        self.session.query().filter().first.return_value = self.user.email
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertEqual(result, self.user.email)
    
    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(username='Test_name', email='any.adress11@gmail.com', password='test_pass')
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)


if __name__ == '__main__':
    unittest.main()