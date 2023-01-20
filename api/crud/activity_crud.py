from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared/', 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared/', 'schemas'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared/', 'db'))

from db_setup import engine, get_db
from activity_schemas import ActivityCreate,ActivityUpdate
from activity_models import Activity

async def get_activity(db: AsyncSession, activity_id: int):
    query = select(Activity).where(Activity.id == activity_id)
    result = db.execute(query)
    return result.scalar_one_or_none()


def get_activities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Activity).offset(skip).limit(limit).all()


def create_activity(db: Session, activity: ActivityCreate):
    db_activity = Activity(
        id=activity.id,
        name=activity.name,
        distance=activity.distance,
        average_speed=activity.average_speed,
        average_heartrate=activity.average_heartrate
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


def delete_activity_by_id(db: Session, activity_id: int):
    query = db.query(Activity).get(activity_id)
    db.delete(query)
    db.commit()
    db.close()
    return None


def update_activity_by_id(db:Session,activity_id,activity: ActivityUpdate):
    db_activity = db.query(Activity).get(activity_id)
    activity_data = activity.dict(exclude_unset=True)
    for key, value in activity_data.items():
        setattr(db_activity, key, value)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    db.close()
    return db_activity