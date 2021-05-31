from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models
from .database import engine, SessionLocal

app = FastAPI()

models.ModelDB.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog')
def create(request:schemas.Blog, db:Session = Depends(get_db)):

    new_blog = models.ModelDB(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db:Session = Depends(get_db)):
    db.query(models.ModelDB).filter(models.ModelDB.id == id).delete(synchronize_session=False)
    db.commit()

    return f"Done, the blog {id} are to delete."


@app.get('/blog')
def all(db: Session = Depends(get_db)):

    blogs = db.query(models.ModelDB).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_201_CREATED)
def show(id:int,  response:Response, db: Session = Depends(get_db)):
    query_blog = db.query(models.ModelDB).filter(models.ModelDB.id == id).first()
    if not query_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is'nt avalible.")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"Detail":f"Blog with id {id} is'nt avalible."}
    return query_blog
