from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models


def get_all(db:Session):
    blogs = db.query(models.ModelDB).all()
    return blogs

def create(request: schemas.Blog, db: Session):
    new_blog = models.ModelDB(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id:int, db:Session):
    blog = db.query(models.ModelDB).filter(models.ModelDB.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The blog {id} not exist.')

    blog.delete(synchronize_session=False)
    db.commit()
    return f"Done, the blog {id} are to delete."

def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.ModelDB).filter(models.ModelDB.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The blog {id} not exist.')

    blog.update(request.dict())
    db.commit()
    return f"Blog witid {id} to are update."


def get_show(id: int, db: Session):
    query_blog = db.query(models.ModelDB).filter(models.ModelDB.id == id).first()
    if not query_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is'nt avalible.")
    return query_blog