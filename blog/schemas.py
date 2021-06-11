from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class BlogBase(BaseModel):

    title : str
    body : str


class Blog(BlogBase):
    class Config():
        orm_mode = True


class User(BaseModel):

    name : str
    email : str
    password : str


class ShowUser(BaseModel):

    name : str
    blogs : List[Blog] = []

    class Config():
        orm_mode = True

class RelationUser(BaseModel):

    name : str

    class Config():
        orm_mode = True


class ShowUserBlog(BaseModel):

    title : str
    body : str
    create_at : datetime
    creator : RelationUser

    class Config():
        orm_mode = True


class ShowBlog(BaseModel):

    title : str
    body : str
    create_at : datetime

    class Config():
        orm_mode = True


class Login(BaseModel):
    usermail: str
    password: str


# JWT
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class EmailData(BaseModel):
    mail : str


class UserID(BaseModel):

    name : str
    id : int

class Comment(BaseModel):

    comment: str

class BaseComment(BaseModel):

    name: str
    body_comment: str
    create_at: datetime


class getComment(BaseComment):

    class Config():

        orm_mode = True


class ShowBlogID(BaseModel):

    title: str
    body: str
    create_at: datetime

    comentarios: List[getComment] = []

    class Config():

        orm_mode = True


class Text(BaseModel):

    text: str