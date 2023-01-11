from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.post import Post
from app.models.user import User
from app.schemas.activity import ActivityCreate, Activity, ActivityUpdate

router = APIRouter()


@router.post("/", status_code=201, response_model=Activity)
def create_activity(
    *,
    activity_in: ActivityCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    post: Post = Depends(deps.get_object_or_404_with_crud(crud.post.get))
):
    """
    Create an activity in the database.
    """
    if current_user.id == post.owner_id:
        raise HTTPException(status_code=403, detail="You are owner of this post")

    try:
        activity = crud.activity.create(db=db, obj_in=activity_in, owner_id=current_user.id, post_id=post.id)
    except IntegrityError:
        raise HTTPException(status_code=403, detail="You are already create activity")

    return activity


@router.put("/{id}", status_code=201, response_model=Activity)
def update_activity(
    activity_in: ActivityUpdate,
    db: Session = Depends(deps.get_db),
    activity: Activity = Depends(deps.check_ownership_model_object_with_crud(crud.activity.get)),
):
    """
    Update activity.
    """
    new_activity = crud.post.update(db, db_obj=activity, obj_in=activity_in)

    return new_activity
