from sqlalcheny import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PATH_DB = 'sqlite:///./blog.db'

engine = create_engine(PATH_DB, connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

