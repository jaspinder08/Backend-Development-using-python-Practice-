from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from config import settings

# Secret key  - Kept on server only
# algorithm
# Expiry time

OAUTH = HTTPBearer()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()
    expiry = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiry})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def verify_access_token(token: HTTPAuthorizationCredentials, credential_exceptions):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credential_exceptions
        return schemas.TokenData(id=user_id)
    except JWTError:
        raise credential_exceptions


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(OAUTH),
    db: Session = Depends(database.get_db),
):
    credential_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f" Could not validate credentials ",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credential_exceptions)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
