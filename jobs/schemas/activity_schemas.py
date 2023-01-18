from typing import Optional

from pydantic import BaseModel


class ActivityBase(BaseModel):
    id: int
    name: str
    distance: float
    average_speed: float
    average_heartrate: float


class ActivityCreate(ActivityBase):
    ...


class Activity(ActivityBase):
    id: int

    class Config:
        orm_mode = True

