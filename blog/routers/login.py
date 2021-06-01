from fastapi import APIRouter, Depends, HTTPException, status
from .. import models, JWT
from sqlalchemy.orm import Session
from ..database import get_db
from ..hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    query_user = db.query(models.UserDB).filter(models.UserDB.email == request.username).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the usermail:{request.username} is invalid.")

    if not Hash.verify(request.password ,query_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password.")


    access_token = JWT.create_access_token( data={"sub": query_user.email} )

    return {"access_token": access_token, "token_type": "bearer"}