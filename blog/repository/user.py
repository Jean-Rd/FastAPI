from .. import schemas, models
from sqlalchemy.orm import Session
from ..hashing import Hash
from fastapi import HTTPException, status

def create(request: schemas.User, db: Session):
    new_user = models.UserDB(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(id: int, db: Session):
    query_user = db.query(models.UserDB).filter(models.UserDB.id == id).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} is'nt avalible.")
    return query_user