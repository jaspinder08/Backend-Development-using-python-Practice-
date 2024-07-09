from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from typing import List, Optional
import models, schemas
import oauth2


router = APIRouter(prefix="/posts", tags=["posts"])


# get all post----------------------------------------------------------------------------------------------------
@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    all_database = (
        db.query(models.Post)
        .filter(models.Post.name.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return all_database


# post data----------------------------------------------------------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# get post using id parameter----------------------------------------------------------------------------------------------------
@router.get(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Post,
)
def get_posts_with_id(id: int, db: Session = Depends(get_db)):
    single_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not single_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    return single_post


# delete post----------------------------------------------------------------------------------------------------
@router.delete(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = deleted_post_query.first()
    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform required actions",
        )

    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post deleted successfully"}


# Update post----------------------------------------------------------------------------------------------------
@router.put(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Post,
)
def update_post(
    id: int,
    postToUpdate: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # Grabbing post with id
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()
    # Graabing the post
    if update_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )

    if updated_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform required actions",
        )
        # update method using dict
    updated_post_query.update(postToUpdate.model_dump(), synchronize_session=False)
    db.commit()
    return updated_post
