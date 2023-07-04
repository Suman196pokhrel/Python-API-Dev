from pydantic import BaseModel, EmailStr, conint, Field
from datetime import datetime
from typing import Optional






class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class PostBase(BaseModel):
    title : str
    content : str
    published: bool = True
    


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: str
    created_at : datetime
    user_id: int

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Posts : Post
    votes: int

    class Config:
        orm_mode = True

class Vote(BaseModel):
    dir: conint(le=1)
    post_id: int


# {
#         "Posts": {
#             "title": "Testing out User Foreign Key toekens",
#             "content": "asdasdCheck out these awesome beaches",
#             "created_at": "2023-05-29T16:09:56.782828+05:45",
#             "id": 10,
#             "user_id": 9,
#             "published": true
#         },
#         "votes": 0
#     },