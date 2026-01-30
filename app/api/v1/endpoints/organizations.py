from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_api_key
from app.crud.organization import organization as org_crud
from app.crud.activity import activity as activity_crud
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationOut

router = APIRouter(dependencies=[Depends(get_api_key)])


@router.get("/", response_model=List[OrganizationOut])
def list_organizations(db: Session = Depends(get_db)):
    return org_crud.get_multi(db)


@router.post("/", response_model=OrganizationOut)
def create_organization(org_in: OrganizationCreate, db: Session = Depends(get_db)):
    return org_crud.create(db, org_in)


@router.get("/{org_id}", response_model=OrganizationOut)
def get_organization(org_id: int, db: Session = Depends(get_db)):
    org = org_crud.get(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.get("/by-building/{building_id}", response_model=List[OrganizationOut])
def organizations_by_building(building_id: int, db: Session = Depends(get_db)):
    return org_crud.get_by_building(db, building_id)


@router.get("/by-activity/{activity_id}", response_model=List[OrganizationOut])
def organizations_by_activity(activity_id: int, db: Session = Depends(get_db)):
    ids = activity_crud.get_with_children_ids(db, activity_id)
    return org_crud.get_by_activity_ids(db, ids)


@router.get("/search/by-name", response_model=List[OrganizationOut])
def organizations_by_name(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return org_crud.get_by_name(db, q)


@router.get("/search/in-radius", response_model=List[OrganizationOut])
def organizations_in_radius(
    lat: float,
    lon: float,
    radius_km: float = Query(1.0, gt=0),
    db: Session = Depends(get_db),
):
    return org_crud.get_in_radius(db, lat=lat, lon=lon, radius_km=radius_km)


@router.get("/search/in-rectangle", response_model=List[OrganizationOut])
def organizations_in_rectangle(
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    db: Session = Depends(get_db),
):
    return org_crud.get_in_rectangle(
        db,
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max,
    )
