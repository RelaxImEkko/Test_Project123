from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.organization import Organization, OrganizationPhone, organization_activities
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


class CRUDOrganization(CRUDBase[Organization, OrganizationCreate, OrganizationUpdate]):
    def create(self, db: Session, obj_in: OrganizationCreate) -> Organization:
        phones = obj_in.phones
        data = obj_in.model_dump(exclude={"phones"})
        db_obj = Organization(**data)
        db.add(db_obj)
        db.flush()
        for phone in phones:
            db.add(OrganizationPhone(organization_id=db_obj.id, phone=phone))
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Organization, obj_in: OrganizationUpdate) -> Organization:
        data = obj_in.model_dump(exclude_unset=True)
        phones = data.pop("phones", None)

        for field, value in data.items():
            setattr(db_obj, field, value)

        if phones is not None:
            db.query(OrganizationPhone).filter(
                OrganizationPhone.organization_id == db_obj.id
            ).delete()
            for phone in phones:
                db.add(OrganizationPhone(organization_id=db_obj.id, phone=phone))

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_building(self, db: Session, building_id: int) -> list[Organization]:
        return (
            db.query(Organization)
            .options(joinedload(Organization.building), joinedload(Organization.activities), joinedload(Organization.phones))
            .filter(Organization.building_id == building_id)
            .all()
        )

    def get_by_activity_ids(self, db: Session, activity_ids: list[int]) -> list[Organization]:
        if not activity_ids:
            return []
        stmt = (
            select(Organization)
            .join(organization_activities, Organization.id == organization_activities.c.organization_id)
            .filter(organization_activities.c.activity_id.in_(activity_ids))
            .options(joinedload(Organization.building), joinedload(Organization.activities), joinedload(Organization.phones))
            .distinct()
        )
        return db.execute(stmt).scalars().all()

    def get_by_name(self, db: Session, name: str) -> list[Organization]:
        return (
            db.query(Organization)
            .filter(func.lower(Organization.name).like(f"%{name.lower()}%"))
            .options(joinedload(Organization.building), joinedload(Organization.activities), joinedload(Organization.phones))
            .all()
        )

    def get_in_radius(
        self,
        db: Session,
        lat: float,
        lon: float,
        radius_km: float,
    ) -> list[Organization]:
        delta = radius_km / 111.0
        from app.models.building import Building

        return (
            db.query(Organization)
            .join(Building, Organization.building_id == Building.id)
            .filter(
                Building.latitude.between(lat - delta, lat + delta),
                Building.longitude.between(lon - delta, lon + delta),
            )
            .options(joinedload(Organization.building), joinedload(Organization.activities), joinedload(Organization.phones))
            .all()
        )

    def get_in_rectangle(
        self,
        db: Session,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
    ) -> list[Organization]:
        from app.models.building import Building

        return (
            db.query(Organization)
            .join(Building, Organization.building_id == Building.id)
            .filter(
                Building.latitude.between(lat_min, lat_max),
                Building.longitude.between(lon_min, lon_max),
            )
            .options(joinedload(Organization.building), joinedload(Organization.activities), joinedload(Organization.phones))
            .all()
        )


organization = CRUDOrganization(Organization)
