from typing import Optional

from pydantic import BaseModel

from app.models.post import ActivityType


class ActivityBase(BaseModel):
    type: ActivityType


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(ActivityBase):
    type: ActivityType


class ActivityInDBBase(ActivityBase):
    id: int
    post_id: int
    owner_id: int

    class Config:
        orm_mode = True


class Activity(ActivityInDBBase):
    pass


class PostInDB(ActivityInDBBase):
    pass
