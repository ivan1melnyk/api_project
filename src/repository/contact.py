from typing import List
import datetime
from datetime import date, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def birthdays_on_this_week(db: Session) -> List[Contact]:
    contacts = db.query(Contact).all()
    today = datetime.date.today()
    weekend = today + timedelta(days=7)
    birthday_list = list()
    for contact in contacts:
        if today < contact.birthday and contact.birthday < weekend:
            birthday_list.append(contact)
    return contacts


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email,
                      number=body.number, birthday=body.birthday, description=body.description)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.number = body.number
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
