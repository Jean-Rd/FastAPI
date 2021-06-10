from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from . import database
from sqlalchemy.orm import relationship
from datetime import datetime

class UserDB(database.Base):

    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at = Column(DateTime, default=datetime.now())

    blogs = relationship('ModelDB', back_populates='creator')


class ModelDB(database.Base):

    __tablename__ = 'Blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    create_at = Column(DateTime, default=datetime.now())

    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)

    creator = relationship('UserDB', back_populates='blogs')
    comment_relation = relationship('CommentsDB', back_populates='blog_relation')


class CommentsDB(database.Base):

    __tablename__ = 'Comments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, ForeignKey('Users.name'))
    body_comment = Column(String, nullable=False)
    blog_id = Column(Integer, nullable=False)
    create_at = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey('Blogs.id'),nullable=False)

    blog_relation = relationship('ModelDB', back_populates='comment_relation')


