from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)


class ContactModel(ContactBase):
    email: str = Field(max_length=50)
    number: str = Field(max_length=15)
    birthday: date
    description: str = Field(max_length=150)


class ContactUpdate(ContactModel):
    email: str = Field(max_length=50)
    number: str = Field(max_length=15)
    birthday: date
    description: str = Field(max_length=150)


class ContactResponse(ContactModel):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
