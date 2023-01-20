from typing import Optional

from pydantic import BaseModel


class ActivityBase(BaseModel):
    id: int
    name: str
    distance: float
    average_speed: float
    average_heartrate: Optional[float]


class ActivityCreate(ActivityBase):
    ...

class ActivityUpdate(BaseModel):
    name: Optional[str]
    distance: Optional[float]
    average_speed: Optional[float]
    average_heartrate: Optional[float]

    class Config:
        orm_mode = True



class Activity(ActivityBase):
    id: int

    class Config:
        orm_mode = True

