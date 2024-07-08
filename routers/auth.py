from fastapi import APIRouter, HTTPException, Response, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database
import schemas
import models
import utils, oauth2


router = APIRouter(
    tags=["auth"],
)


@router.post(
    "/login",
    response_model=schemas.Token,
)
def login(
    user_credentials: schemas.UserLogin,
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Password"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {
        "data": "Login Successfull",
        "access_token": access_token,
        "token_type": "bearer",
    }
