from sqlalchemy import Column, Integer, String, ForeignKey
from . import database
from sqlalchemy.orm import relationship

class ModelDB(database.Base):

    __tablename__ = 'Blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)

    user_id = Column(Integer, ForeignKey('Users.id'))

    creator = relationship("UserDB", back_populates="blogs")


class UserDB(database.Base):

    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship('ModelDB', back_populates="creator")
