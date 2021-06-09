from fastapi import APIRouter, Depends, status, Response
from .. import schemas, oauth
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Dict
from ..repository import blog


router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


@router.post('/')
def create(request: schemas.Blog,db: Session = Depends(get_db), token: str = Depends(oauth.oauth2_scheme)
           ,curent_user: schemas.User = Depends(oauth.get_current_user)):

    return blog.create(request, db, token)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, password_confirm: str,db:Session = Depends(get_db), token: str = Depends(oauth.oauth2_scheme),
            curent_user: schemas.User = Depends(oauth.get_current_user)):
    return Response(blog.destroy(id, db, password_confirm, token))


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, password_confirm: str,request: schemas.Blog, db:Session = Depends(get_db), token: str = Depends(oauth.oauth2_scheme),
           curent_user: schemas.User = Depends(oauth.get_current_user)):
    return blog.update(id, password_confirm, request, db, token)


@router.get('/', response_model=List[schemas.ShowUserBlog])
def all(db: Session = Depends(get_db) , token: str = Depends(oauth.oauth2_scheme)
        ,curent_user: schemas.User = Depends(oauth.get_current_user)):
    return blog.get_all(db, token)


@router.get('/{blog_name}', status_code=200, response_model=List[schemas.ShowBlog])
def show(blog_name: str, db: Session = Depends(get_db), curent_user: schemas.User = Depends(oauth.get_current_user)):
    return blog.get_show(blog_name, db)

