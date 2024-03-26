from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse
from src.repository import contact as repository_contact


router = APIRouter(prefix='/current_birthday', tags=["current_birthday"])


@router.get("/", response_model=List[ContactResponse])
async def birthdays_on_this_week(db: Session = Depends(get_db)):
    contacts = await repository_contact.birthdays_on_this_week(db)
    return contacts
