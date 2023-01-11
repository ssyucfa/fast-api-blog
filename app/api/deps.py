from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm.session import Session

from app.core.auth import oauth2_scheme
from app.core.config import settings
from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.post import Post


class TokenData(BaseModel):
    username: Optional[str] = None


def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


def get_object_or_404_with_crud(crud_get_object):
    def get_object_or_404(id: int, db: Session = Depends(get_db)) -> Base:
        model_object = crud_get_object(db, id=id)
        if model_object is None:
            raise HTTPException(status_code=404, detail="Post not found")

        return model_object
    return get_object_or_404


def check_ownership_model_object_with_crud(crud_get_object):
    def get_ownership_model_object(
        model_object: Base = Depends(get_object_or_404_with_crud(crud_get_object)),
        current_user: User = Depends(get_current_user)
    ) -> Base:
        if model_object.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Forbidden")

        return model_object
    return get_ownership_model_object
