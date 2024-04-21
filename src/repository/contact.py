from typing import List
import datetime

from datetime import date, timedelta


from sqlalchemy.orm import Session
from sqlalchemy import or_

import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "....")))

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()


async def search(search: str, user: User, db: Session) -> Contact:
    """
    Search for contacts by first name, last name, or email address.

    :param search: The search string to match against first name, last name, or email address.
    :type search: str
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts matching the search criteria.
    :rtype: List[Contact]
    """
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
    """
    Retrives a list of contacts that have birthday in the next week

    :param skip: The number of contact to skip
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for
    :type user: User
    :return: A list of contacts that have birthdays in the next week
    :rtype: List[Contact]
    """
    contacts_with_birthdays = []
    today = date.today()
    current_year = today.year
    contacts = db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()
    for contact in contacts:
        td = contact.birthday.replace(year=current_year) - today
        if 0 <= td.days <= 7:
            contacts_with_birthdays.append(contact)
        else:
            continue
    return contacts_with_birthdays


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactModel
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email,
                      number=body.number, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactUpdate
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
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
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
