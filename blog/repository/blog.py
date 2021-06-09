from fastapi import HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, models
from ..JWT import email_token
from ..hashing import Hash

def get_all(db: Session, token: str):

    email = email_token(token)
    id = db.query(models.UserDB.id).filter(models.UserDB.email == email).first()

    if not id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="JWT invalid.")

    blogs = db.query(models.ModelDB).filter(models.ModelDB.user_id == id[0]).all()
    return blogs

def create(request: schemas.Blog, db: Session, token: str):

    email = email_token(token)
    current_id = db.query(models.UserDB.id).filter(models.UserDB.email == email).first()

    if not current_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pagina no disponible.")

    new_blog = models.ModelDB(title=request.title, body=request.body, user_id=current_id[0])
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id: int, db:Session, password_confirm: str, token: str):

    email = email_token(token)

    auth_email = db.query(models.UserDB).filter(models.UserDB.email == email).first()

    if not auth_email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="JWT invalid.")

    hash_password = db.query(models.UserDB.password).filter(models.UserDB.email == email).first()

    if not Hash.verify(password_confirm, hash_password[0]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect password.")

    id_email: int = db.query(models.UserDB.id).filter(models.UserDB.email == email).first()

    users_ids = db.query(models.ModelDB.id).filter(models.ModelDB.user_id == id_email[0]).all()

    if not id in set().union(*users_ids):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'ID:{id} incorrecto.')


    blog = db.query(models.ModelDB).filter(models.ModelDB.id == id)
    blog.delete(synchronize_session=False)
    db.commit()
    return f"El blog con id:{id} ah sido eliminado."

def update(id: int, password_confirm: str, request: schemas.Blog, db: Session, token: str):

    email = email_token(token)

    auth_email = db.query(models.UserDB).filter(models.UserDB.email == email).first()

    if not auth_email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the usermail:{email} is invalid.")

    hash_password = db.query(models.UserDB.password).filter(models.UserDB.email == email).first()

    if not Hash.verify(password_confirm, hash_password[0]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password.")

    id_email = db.query(models.UserDB.id).filter(models.UserDB.email == email).first()

    users_ids = db.query(models.ModelDB.id).filter(models.ModelDB.user_id == id_email[0]).all()

    if not id in set().union(*users_ids):

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The blog {id} not exist.')

    blog = db.query(models.ModelDB).filter(models.ModelDB.id == id)
    blog.update(request.dict())
    db.commit()
    return f"El blog con id:{id} ah sido actualizado."


def get_show(blog_name: str, db: Session):

    query_blog = db.query(models.ModelDB).filter(models.ModelDB.title == blog_name).all()

    if not query_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with name {blog_name} is'nt avalible.")

    return query_blog
