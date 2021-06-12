from fastapi import APIRouter, Depends
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..repository import user
from .. import oauth


router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post('/', response_model=schemas.UserCreator)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/{id}',response_model=schemas.ShowUser)
def get_user(id:int, db: Session = Depends(get_db), curent_user: schemas.User = Depends(oauth.get_current_user)):
    return user.get_user(id, db)