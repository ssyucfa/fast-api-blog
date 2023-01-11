from app.crud.base import CRUDBase
from app.models.post import Activity
from app.schemas.activity import ActivityUpdate, ActivityCreate


class CRUDActivity(CRUDBase[Activity, ActivityCreate, ActivityUpdate]):
    ...


activity = CRUDActivity(Activity)
