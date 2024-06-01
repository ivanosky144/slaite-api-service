from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.eventModel import Event
from models.taskModel import Task
from models.userModel import User
from models.scheduleModel import Schedule
from models.activityModel import Activity
from config.database import get_db
from middleware.authentication import verifyAuth
from datetime import date


router = APIRouter(tags=["Activities"])

@router.get("/{schedule_id}", dependencies=[Depends(verifyAuth)])
def getAllActivitesBySchedule(schedule_id: int, db: Session=Depends(get_db)):
    activities = db.query(Activity).filter(Activity.schedule_id == schedule_id)

    if not activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return {
        "status": "success",
        "data": activities
    }

@router.get("/user/{user_email}", dependencies=[Depends(verifyAuth)])
def getActivities(user_email: str, db: Session=Depends(get_db), start_date: str = Query(None), end_date: str = Query(None)):
    existing_user = db.query(User).filter(User.email == user_email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="Target user not found")

    activities_query = db.query(Activity).filter(Activity.schedule.has(user_id=existing_user.id))

    if start_date:
        activities_query = activities_query.filter(Activity.date >= date.strptime(start_date, '%Y-%m-%d').date())
    
    if end_date:
        activities_query = activities_query.filter(Activity.date <= date.strptime(end_date, '%Y-%m-%d').date())

    activities = activities_query.all()

    activities_data = [{
        "id": activity.id,
        "date": activity.date,
        "repeat_interval": activity.repeat_interval,
        "schedule_id": activity.schedule_id,
        "created_at": activity.created_at,
        "updated_at": activity.updated_at
    } for activity in activities]

    return {
        "status": "success",
        "data": activities_data
    }

