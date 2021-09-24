from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get('/')
def index():
    return {'Data': {'Name': "Jean"}}


@app.get('/about')
def about():
    return {'Data_about': {"Pagina acerca...": [{'1': 'Jean', "2": 'Victor', '3': 'Rada'}]}}


@app.get('/blog')
def blog(limit=10, published:bool=True, sort: Optional[str]=None):
    if published:
        return {'Data': f"{limit} post published"}
    else:
        return {"Data": "No published"}


@app.get('/blog/unpublished')
def unpublished():
    return {"Data": 'All unplublished blog'}


# ESTRUCTURA DINAMICA CON SHOW
@app.get('/blog/{id}')
def show(id: int):
    return {'Data': id}


@app.get('/blog/{id}/comments')
def comments(id: int , limit=30):
    # Comentario del user {id}
    return {'Data': {'a)': '1', 'b)': '2', 'c)': '3'}, "Limit": limit, 'ID': id}


class Blog(BaseModel):
    title : str
    body : str
    published : Optional[bool]


@app.post('/blog')
def create_blog(request:Blog):
    # blog:Blog
    return {'data': f"{request.title} is title of the Blog.\n{request.body}"}

