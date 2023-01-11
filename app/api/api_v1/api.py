from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, post, activity


api_router = APIRouter()
api_router.include_router(post.router, prefix="/posts", tags=["posts"])
api_router.include_router(activity.router, prefix="/activities", tags=["activities"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
