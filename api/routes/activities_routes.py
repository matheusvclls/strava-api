from typing import List
import os
import sys

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'crud'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared/', 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared/', 'schemas'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared/', 'db'))

from activity_schemas import ActivityCreate, ActivityUpdate, Activity
from activity_crud import get_activity, create_activity,delete_activity_by_id, update_activity_by_id, get_activities, get_longest_activity,get_activities_from_this_week,get_activities_from_this_week_starting_from_monday, get_total_running_actitivities, get_total_kms_running_this_week
from db_setup import get_db

router = fastapi.APIRouter()


@router.get("/activities", response_model=List[Activity])
async def read_activities(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    activities = get_activities(db, skip=skip, limit=limit)
    return activities


@router.post("/activities/", response_model=Activity, status_code=201)
async def create_new_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    db_activity = await get_activity(db=db, activity_id=activity.id)
    if db_activity:
        raise HTTPException(
            status_code=400, detail="ID is already registered"
        )
    return create_activity(db=db, activity=activity)


@router.get("/activities/{activity_id}", response_model=Activity)
async def read_activity(activity_id: int,db: Session = Depends(get_db)):
    db_activity = await get_activity(db=db, activity_id=activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

@router.delete('/activity/{activity_id}', response_model=str)
async def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = await get_activity(db=db, activity_id=activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    delete_activity_by_id(db=db,activity_id=activity_id)
    return f"Activity {activity_id} deleted successfully"

@router.patch("/activity/{activity_id}", response_model=Activity)
async def update_activity(activity_id: int, activity: ActivityUpdate, db: Session = Depends(get_db)):
    db_activity = await get_activity(db=db, activity_id=activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    db_activity = update_activity_by_id(db=db,activity_id=activity_id, activity=activity)
    
    return db_activity

@router.get("/metrics/logest_activity")
async def longest_activity(db: Session = Depends(get_db)):
    db_activity = await get_longest_activity(db=db)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Table is empty")
    return db_activity


@router.get("/metrics/activities_from_this_week")
async def activities_from_this_week(db: Session = Depends(get_db)):
    db_activity = await get_activities_from_this_week(db=db)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Table is empty")
    return db_activity


@router.get("/metrics/activities_from_this_week_starting_from_monday")
async def activities_from_this_week_starting_from_monday(db: Session = Depends(get_db)):
    db_activity = await get_activities_from_this_week_starting_from_monday(db=db)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Table is empty")
    return db_activity

@router.get("/metrics/total_running_actitivities", response_model = int)
async def total_running_actitivities(db: Session = Depends(get_db)):
    db_activity = await get_total_running_actitivities(db=db)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Table is empty")
    return db_activity

@router.get("/metrics/total_kms_running_this_week")
async def total_kms_running_this_week(db: Session = Depends(get_db)):
    db_activity = await get_total_kms_running_this_week(db=db)
    if db_activity is None:
        return 0
    return db_activity

