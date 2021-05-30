from fastapi import FastAPI
from . import schemas, models
from .database import engine

app = FastAPI()

models.ModelDB.metadata.create_all(engine)

@app.post('/blog')
def create(request:schemas.Blog, db):
    return db
