from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class SamplePost(BaseModel):
    name: str
    age: int
    salary: float
    salary_received: bool = True


class PostCreate(SamplePost):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Response(SamplePost):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class User(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
