from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint


class SamplePost(BaseModel):
    caption: str
    tagged_people: int
    music_name: str
    is_influencer: bool = True


class PostCreate(SamplePost):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Post(SamplePost):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


# class PostOut(BaseModel):
#     Post: Post
#     votes: int

#     class Config:
#         from_attributes = True


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


class Votes(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)  # Constraint for direction: 0 or 1
