from sqlalchemy.orm import Session
from .. import models, schemas
from ..JWT import email_token
from fastapi import HTTPException, status

def create_comment(token: str, blog_id: int, request: schemas.Comment, db: Session):

    email = email_token(token)
    current_id = db.query(models.UserDB.id).filter(models.UserDB.email == email).first()
    current_user = db.query(models.UserDB.name).filter(models.UserDB.email == email).first()

    if not current_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pagina no disponible.")

    new_comment = models.CommentsDB(name = current_user[0],body_comment=request.comment, blog_id=blog_id, user_id=current_id[0])

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment
