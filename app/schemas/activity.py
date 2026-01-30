from pydantic import BaseModel


class ActivityBase(BaseModel):
    name: str
    parent_id: int | None = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(ActivityBase):
    pass


class ActivityInDBBase(ActivityBase):
    id: int

    class Config:
        from_attributes = True


class Activity(ActivityInDBBase):
    pass
