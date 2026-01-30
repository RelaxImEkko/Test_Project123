from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_api_key
from app.crud.activity import activity as activity_crud
from app.schemas.activity import Activity, ActivityCreate, ActivityUpdate

router = APIRouter(dependencies=[Depends(get_api_key)])


@router.get("/", response_model=List[Activity])
def list_activities(db: Session = Depends(get_db)):
    return activity_crud.get_multi(db)


@router.post("/", response_model=Activity)
def create_activity(activity_in: ActivityCreate, db: Session = Depends(get_db)):
    if activity_in.parent_id is not None:
        ok = activity_crud.can_create_with_parent(db, activity_in.parent_id)
        if not ok:
            raise HTTPException(status_code=400, detail="Max activity depth is 3 levels")
    return activity_crud.create(db, activity_in)


@router.get("/{activity_id}", response_model=Activity)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    return activity_crud.get(db, activity_id)


@router.put("/{activity_id}", response_model=Activity)
def update_activity(
    activity_id: int,
    activity_in: ActivityUpdate,
    db: Session = Depends(get_db),
):
    db_obj = activity_crud.get(db, activity_id)
    if activity_in.parent_id is not None:
        ok = activity_crud.can_create_with_parent(db, activity_in.parent_id)
        if not ok:
            raise HTTPException(status_code=400, detail="Max activity depth is 3 levels")
    return activity_crud.update(db, db_obj, activity_in)
