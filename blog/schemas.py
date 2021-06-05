from pydantic import BaseModel
from typing import Optional


class BlogBase(BaseModel):

    title : str
    body : str
    password: str


class Blog(BlogBase):
    class Config():
        orm_mode = True


class User(BaseModel):

    name : str
    email : str
    password : str


class ShowUser(BaseModel):

    name : str
    email : str
    #blogs : List[Blog] = []

    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    # show all mejorar ^ show id para que muestre solo uno
    title : str
    body : str
    creator : ShowUser
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

