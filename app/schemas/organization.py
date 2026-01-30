from typing import List

from pydantic import BaseModel

from app.schemas.building import Building
from app.schemas.activity import Activity


class OrganizationPhoneOut(BaseModel):
    phone: str

    class Config:
        from_attributes = True


class OrganizationBase(BaseModel):
    name: str
    building_id: int
    phones: List[str]


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: str | None = None
    building_id: int | None = None
    phones: List[str] | None = None


class OrganizationOut(BaseModel):
    id: int
    name: str
    building_id: int
    building: Building | None = None
    activities: List[Activity] = []
    phones: List[OrganizationPhoneOut] = []

    class Config:
        from_attributes = True
