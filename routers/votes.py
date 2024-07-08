from fastapi import status, HTTPException, Depends, APIRouter
import schemas, models, database, oauth2
from database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Votes, db: Session = Depends(get_db)):
    return "Hello"
