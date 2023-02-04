from sqlalchemy.orm import Session
import sys
import os 


sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared/', 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared/', 'schemas'))

from activity_schemas import ActivityCreate
from activity_models import Activity


def get_strava_activity(db: Session, activity_id: int):
    result = db.query(Activity).filter(Activity.id == activity_id).first()
    return result


def create_activity(db: Session, activity: ActivityCreate):
    db_activity = Activity(
        id=activity['id'],
        name=activity['name'],
        distance=activity['distance'],
        average_speed=activity['average_speed'],
        average_heartrate=activity['average_heartrate'],
        start_date=activity['start_date']
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


