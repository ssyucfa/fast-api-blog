from typing import Any, Optional

from sqlalchemy import func, case
from sqlalchemy.orm import Session, aliased

from app.crud.base import CRUDBase
from app.models.post import Post, Activity, ActivityType
from app.schemas.post import PostCreate, PostUpdate, PostWithActivities, ListPosts


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    def _get_query_with_activities(self, db: Session):
        sq_activities = db.query(
            Activity.post_id,
            func.count(case(
                [
                    (Activity.type == ActivityType.LIKE, 1)
                ],
            )).label("likes"),
            func.count(case(
                [
                    (Activity.type == ActivityType.DISLIKE, 1)
                ]
            )).label("dislikes")
        ).group_by(Activity.post_id).subquery()

        return db.query(
            self.model,
            sq_activities.c.likes.label("likes"),
            sq_activities.c.dislikes.label("dislikes")
        ).outerjoin(sq_activities, self.model.id == sq_activities.c.post_id)

    def get_post_with_activities(self, db: Session, id: int) -> PostWithActivities:
        post_with_activities = self._get_query_with_activities(db).filter(self.model.id == id).first()
        return PostWithActivities(
            title=post_with_activities.Post.title,
            description=post_with_activities.Post.description,
            owner_id=post_with_activities.Post.owner_id,
            id=post_with_activities.Post.id,
            likes=post_with_activities.likes,
            dislikes=post_with_activities.dislikes
        )

    def get_posts_with_activities(self, db: Session) -> ListPosts:
        posts_with_activities = []
        for post_with_activities in self._get_query_with_activities(db).all():
            posts_with_activities.append(
                PostWithActivities(
                    title=post_with_activities.Post.title,
                    description=post_with_activities.Post.description,
                    owner_id=post_with_activities.Post.owner_id,
                    id=post_with_activities.Post.id,
                    likes=post_with_activities.likes,
                    dislikes=post_with_activities.dislikes
                )
            )

        return ListPosts(posts=posts_with_activities)


post = CRUDPost(Post)
