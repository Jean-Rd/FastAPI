from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from . import database
from sqlalchemy.orm import relationship, backref
from datetime import datetime

class UserDB(database.Base):

    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String(30), nullable=False)
    create_at = Column(DateTime, default=datetime.now())

    blogs = relationship('ModelDB', back_populates='creator')


class ModelDB(database.Base):

    __tablename__ = 'Blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)

    create_at = Column(DateTime, default=datetime.now())

    creator = relationship('UserDB', back_populates='blogs')


class CommentsDB(database.Base):

    __tablename__ = 'Comments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    body_comment = Column(String, nullable=False)
    blog_id = Column(Integer, ForeignKey('Blogs.id'))
    user_id = Column(Integer, nullable=False)

    create_at = Column(DateTime, default=datetime.now())

    blog_relation = relationship('ModelDB', backref=backref('comentarios', lazy = True))



