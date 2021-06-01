from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter()

@router.post('/user', response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.UserDB(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user/{id}',response_model=schemas.ShowUser, tags=['users'])
def get_user(id:int, db: Session = Depends(get_db)):
    query_user = db.query(models.UserDB).filter(models.UserDB.id == id).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} is'nt avalible.")
    return query_user