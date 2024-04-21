import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.repository.contact import (
    get_contacts, get_contact, create_contact, remove_contact, update_contact, get_contacts_birthdays, search
)

from src.schemas import ContactModel, ContactUpdate
from src.database.models import Contact, User
import unittest
from unittest.mock import MagicMock
import datetime
from sqlalchemy.orm import Session


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(first_name='test_firstname', last_name='test_lastname', email='test contact',
                            number='0111111111', user_id=1)
        self.session.query().filter().all.return_value = self.user
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.number, body.number)
        self.assertEqual(result.user_id, body.user_id)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        contact = Contact(id=1, first_name='test_firstname', last_name='test_lastname', email='any.adress11@gmail.com', number='0111111111', birthday=datetime.date(2000, 11, 11), description='test description', user_id=self.user.id)
        # Creating a ContactUpdate object with all required fields
        body = ContactUpdate(
            email='new.email@gmail.com',
            number='0222222222',
            birthday=datetime.date(2000, 11, 11),
            description='updated description',
            user_id=self.user.id,  # Assuming user_id is required for update
            first_name='UpdatedFirstname',  # Adding required fields from ContactBase
            last_name='UpdatedLastname'  # Adding required fields from ContactBase
        )
        self.session.query().filter().first.return_value = contact
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactUpdate(
            email='any11@email.com',
            number='0111111111',
            birthday=datetime.date(2000, 11, 11),
            description='test description',
            first_name='test_firstname',  # Add required fields from ContactBase
            last_name='test_lastname',  # Add required fields from ContactBase
            user_id=self.user.id  # Add required field from ContactModel
        )
        # Mocking the behavior when no contact is found
        self.session.query().filter().first.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        # Asserting that the result is None
        self.assertIsNone(result)

    async def test_get_contacts_birthdays(self):
        contact = Contact(birthday=datetime.date.today(), user_id=self.user.id)
        self.session.query().filter().offset().limit().all.return_value = [contact]
        result = await get_contacts_birthdays(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, [contact])

    async def test_get_contacts_birthdays_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contacts_birthdays(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, [])

    async def test_search(self):
        contact = Contact(first_name='Testname', user_id=self.user.id)
        # Assuming self.session is a mock object
        self.session.query.return_value.filter.return_value.all.return_value = [contact]
        
        first_name_search = 'Testname'
        result = await search(search=first_name_search, user=self.user, db=self.session)
        self.assertEqual(result, [contact])

    async def test_search_not_found(self):
        # Mocking the behavior of an empty result set
        self.session.query.return_value.filter.return_value.all.return_value = []
        first_name_search = 'Testname'
        result = await search(search=first_name_search, user=self.user, db=self.session)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
