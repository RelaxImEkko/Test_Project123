from pydantic import BaseModel


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BuildingBase):
    pass


class BuildingInDBBase(BuildingBase):
    id: int

    class Config:
        from_attributes = True


class Building(BuildingInDBBase):
    pass
