from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_api_key
from app.crud.building import building as building_crud
from app.schemas.building import Building, BuildingCreate, BuildingUpdate

router = APIRouter(dependencies=[Depends(get_api_key)])


@router.get("/", response_model=List[Building])
def list_buildings(db: Session = Depends(get_db)):
    return building_crud.get_multi(db)


@router.post("/", response_model=Building)
def create_building(building_in: BuildingCreate, db: Session = Depends(get_db)):
    return building_crud.create(db, building_in)


@router.get("/{building_id}", response_model=Building)
def get_building(building_id: int, db: Session = Depends(get_db)):
    return building_crud.get(db, building_id)


@router.put("/{building_id}", response_model=Building)
def update_building(
    building_id: int,
    building_in: BuildingUpdate,
    db: Session = Depends(get_db),
):
    db_obj = building_crud.get(db, building_id)
    return building_crud.update(db, db_obj, building_in)
