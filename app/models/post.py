import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    description = Column(String(256), index=True, nullable=True)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="posts")
    activities = relationship(
        "Activity",
        cascade="all,delete-orphan",
        back_populates="post",
        uselist=True,
    )


class ActivityType(int, enum.Enum):
    LIKE = 1
    DISLIKE = 2


class Activity(Base):
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(ActivityType), nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User")
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False, unique=True)
    post = relationship("Post", back_populates="activities")

    __table_args__ = (
        UniqueConstraint('owner_id', 'post_id'),
    )
