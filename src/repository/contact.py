from typing import List
import datetime
from datetime import date, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()


async def search(search: str, user: User, db: Session) -> Contact:
    contacts = db.query(Contact).filter(Contact.user_id == user.id,
                                        or_(
                                            Contact.first_name.like(
                                                f"%{search}%"),
                                            Contact.last_name.like(
                                                f"%{search}%"),
                                            Contact.email.like(f"%{search}%")
                                        )
                                        ).all()

    return contacts


async def get_contacts_birthdays(skip: int, limit: int, user: User, db: Session):
    contacts_with_birthdays = []
    today = date.today()
    current_year = today.year
    contacts = db.query(Contact).filter(Contact.user_id ==
                                        user.id).offset(skip).limit(limit).all()
    for contact in contacts:
        td = contact.birthday.replace(year=current_year) - today
        if 0 <= td.days <= 7:
            contacts_with_birthdays.append(contact)
        else:
            continue
    return contacts_with_birthdays


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email,
                      number=body.number, birthday=body.birthday, description=body.description, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(
        Contact.id == contact_id, Contact.user_id == user.id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.number = body.number
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
