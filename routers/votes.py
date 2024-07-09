from fastapi import status, HTTPException, Depends, APIRouter
import schemas, models, database, oauth2
from database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Votes,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    posts = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {vote.id} doesn't exist",
        )
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with {current_user.id} has already liked the {vote.post_id}",
            )
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {
            "message": " Successfully, Liked the post",
        }
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Vote doesnot exist",
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {
            "message": "Successfully Deleted Like",
        }
