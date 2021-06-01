from fastapi import FastAPI, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from . import schemas, models
from .database import engine, SessionLocal
from .hashing import Hash

app = FastAPI()

models.ModelDB.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', tags=['blogs'])
def create(request:schemas.Blog, db:Session = Depends(get_db)):

    new_blog = models.ModelDB(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy(id:int, db:Session = Depends(get_db)):
    blog = db.query(models.ModelDB).filter(models.ModelDB.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The blog {id} not exist.')

    blog.delete(synchronize_session=False)
    db.commit()
    return f"Done, the blog {id} are to delete."


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id:int, request: schemas.Blog, db:Session = Depends(get_db)):
    blog = db.query(models.ModelDB).filter(models.ModelDB.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The blog {id} not exist.')

    blog.update(request.dict())
    db.commit()
    return f"Blog witid {id} to are update."


@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def all(db: Session = Depends(get_db)):

    blogs = db.query(models.ModelDB).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog, tags=['blogs'])
def show(id:int, db: Session = Depends(get_db)):
    query_blog = db.query(models.ModelDB).filter(models.ModelDB.id == id).first()
    if not query_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is'nt avalible.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f"Blog with id {id}:is'nt avalible."}
    return query_blog


@app.post('/user', response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.UserDB(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}',response_model=schemas.ShowUser, tags=['users'])
def get_user(id:int, db: Session = Depends(get_db)):
    query_user = db.query(models.UserDB).filter(models.UserDB.id == id).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} is'nt avalible.")
    return query_user