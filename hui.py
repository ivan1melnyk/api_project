import datetime
from datetime import date, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field


class Contact(BaseModel):
    name: str = Field(max_length=50)
    birthday: date


contact1 = Contact(name='Ivan', birthday='2024-03-28')
contact2 = Contact(name='Myron', birthday='2024-03-29')

contacts = [contact1, contact2]

print('@##Contacts:', contacts)

today = datetime.date.today()
weekend = today + timedelta(days=7)

birthday_list = []

for contact in contacts:
    if today < contact.birthday and contact.birthday < weekend:
        birthday_list.append(contact)

print(birthday_list)
