from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    description: Optional[str]


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    title: Optional[str]


class PostInDBBase(PostBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class Post(PostInDBBase):
    pass


class PostWithActivities(PostInDBBase):
    likes: Optional[int] = 0
    dislikes: Optional[int] = 0


class PostInDB(PostInDBBase):
    pass


class ListPosts(BaseModel):
    posts: list[PostWithActivities]
