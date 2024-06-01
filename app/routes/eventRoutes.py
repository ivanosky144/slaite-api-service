from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.eventModel import Event
from models.activityModel import Activity
from models.scheduleModel import Schedule
from models.userModel import User
from dto.eventObjects import EventBody
from config.database import get_db
from datetime import datetime
from middleware.authentication import verifyAuth

router = APIRouter(tags=["Events"])

@router.get("/{event_id}", dependencies=[Depends(verifyAuth)])
def getEventDetail(event_id: int, db: Session=Depends(get_db)):
    event_detail = db.query(Event).get(event_id)
    if not event_detail:
        raise HTTPException(status_code=404, detail="Event not found")
    
    activity_data = db.query(Activity).get(event_detail.activity_id)

    payload = {
        "title": event_detail.title,
        "description": event_detail.description,
        "schedule_id": activity_data.schedule_id,
        "repeat_interval": activity_data.repeat_interval,
        "date": activity_data.date,
        "start_time": event_detail.start_time,
        "end_time": event_detail.end_time
    }

    return {
        "status": "success",
        "data": payload
    }

@router.post("/", dependencies=[Depends(verifyAuth)])
def createEvent(event: EventBody, db: Session=Depends(get_db)):

    used_schedule = db.query(Schedule).filter(Schedule.id == event.schedule_id)

    if not used_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    new_activity = Activity(
        date = event.date,
        repeat_interval = event.repeat_interval,
        schedule_id = event.schedule_id,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)

    new_event = Event(
        title = event.title,
        description = event.description,
        start_time = event.start_time,
        end_date = event.end_time,
        activity_id = new_activity.id,
        created_at = new_activity.created_at,
        updated_at = new_activity.updated_at
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {
        "status": "success",
        "message": "New event has been created"
    }

@router.put("/{event_id}", dependencies=[Depends(verifyAuth)])
def updateEvent():
    return

@router.delete("/{event_id}", dependencies=[Depends(verifyAuth)])
def deleteEvent():
    return

@router.get("/user/{user_email}", dependencies=[Depends(verifyAuth)])
def getEventsByUser(user_email: str, db: Session=Depends(get_db), start_date: str = Query(None), end_date: str = Query(None)):
    existing_user = db.query(User).filter(User.email == user_email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="Target user not found")
    
    events = db.query(Event, Activity).join(Activity).filter(Activity.schedule.has(user_id=existing_user.id)).all()

    event_activities = [{
        "date": activity.date,
        "repeat_interval": activity.repeat_interval,
        "activity_id": activity.id,
        "id": event.id,
        "title": event.title,
        "start_time": event.start_time,
        "end_time": event.end_time,
        "created_at": event.created_at,
        "updated_at": event.updated_at
    } for event, activity in events]
    
    return {
        "status": "success",
        "data": event_activities
    }