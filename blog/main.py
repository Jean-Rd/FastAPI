from fastapi import FastAPI
import uvicorn
from . import schemas

app = FastAPI()

@app.post('/blog')
def create(request:schemas.Blog):
    return request
