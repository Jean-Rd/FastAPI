from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .JWT import verify_token

# De donde desea obtener el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# OAuth2PasswordBearer es el formulario donde se pide el login del usuario;
# el username y password se envian a una url especifica declarado por OAuth2PasswordBearer.tokenUrl


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)
