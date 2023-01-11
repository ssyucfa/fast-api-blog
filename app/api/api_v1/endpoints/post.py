from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.post import Post, PostCreate, ListPosts, PostUpdate, PostWithActivities

router = APIRouter()


@router.post("/", status_code=201, response_model=Post)
def create_post(
    *, post_in: PostCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)
):
    """
    Create a new post in the database.
    """
    post = crud.post.create(db=db, obj_in=post_in, owner_id=current_user.id)

    return post


@router.get("/", status_code=200, response_model=ListPosts)
def list_post(
    *, db: Session = Depends(deps.get_db)
):
    """
    List post.
    """
    posts = crud.post.get_posts_with_activities(db)

    return posts


@router.get("/{id}", status_code=200, response_model=PostWithActivities)
def detail_post(
    post_with_activities: PostWithActivities = Depends(
        deps.get_object_or_404_with_crud(crud.post.get_post_with_activities)
    )
):
    """
    Detail post.
    """
    return post_with_activities


@router.put("/{id}", status_code=201, response_model=Post)
def update_post(
    post_in: PostUpdate,
    db: Session = Depends(deps.get_db),
    post: Post = Depends(deps.get_object_or_404_with_crud(crud.post.get)),
):
    """
    Update post.
    """
    new_post = crud.post.update(db, db_obj=post, obj_in=post_in)

    return new_post


@router.delete("/{id}", status_code=204)
def delete_post(
    db: Session = Depends(deps.get_db),
    post: Post = Depends(deps.check_ownership_model_object_with_crud(crud.post.get))
):
    """
    Delete post.
    """
    crud.post.delete(db, id=post.id)
