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


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
