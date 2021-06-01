from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models
from sqlalchemy.orm import Session
from ..database import get_db
from ..hashing import Hash

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    query_user = db.query(models.UserDB).filter(models.UserDB.email == request.usermail).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the usermail:{request.usermail} is invalid.")

    if not Hash.verify(request.password, query_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password.")

    return query_user