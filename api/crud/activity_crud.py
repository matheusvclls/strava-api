from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import functions
from datetime import datetime, timedelta
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

async def get_longest_activity(db:Session):
    query = select(Activity).order_by(Activity.distance.desc()).limit(1)
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
        average_heartrate=activity.average_heartrate,
        start_date=activity.start_date
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

async def get_activities_from_this_week(db:Session):

    today = datetime.now()
    
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    activities = db.query(Activity).filter(
        Activity.start_date >= start_of_week,
        Activity.start_date <= end_of_week
    ).all()

    return activities

async def get_activities_from_this_week_starting_from_monday(db:Session):
    monday = datetime.today() - timedelta(days=datetime.today().weekday())
    activities = db.query(Activity).filter(Activity.start_date >= monday).all()

    return activities


async def get_total_kms_running_this_week(db:Session):
    monday = datetime.today() - timedelta(days=datetime.today().weekday())
    activities = db.query(functions.sum(Activity.distance).label("mySum")).filter(Activity.start_date >= monday).first()

    return activities.mySum

async def get_total_running_actitivities(db:Session):
    activities = db.query(Activity).count()

    return activities

async def get_last_five_running_actitivities(db:Session):
    activities = db.query(Activity).order_by(Activity.start_date.desc()).limit(5).all()

    return activities