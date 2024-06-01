from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session
from models.scheduleModel import Schedule
from models.activityModel import Activity
from models.notificationModel import Notification
from models.taskModel import Task
from models.eventModel import Event
from models.userModel import User
from dto.scheduleObjects import ScheduleBody
from datetime import datetime
from config.database import get_db
from middleware.authentication import verifyAuth

router = APIRouter(tags=["Schedules"])

@router.post("/", dependencies=[Depends(verifyAuth)])
def createSchedule(schedule: ScheduleBody, db: Session=Depends(get_db)):
    new_schedule = Schedule(
        name = schedule.name,
        user_id = schedule.user_id,
        color = schedule.color,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)

    if schedule.activities:
        for activity_data in schedule.activities:
            new_activity = Activity(
                date = activity_data.date,
                repeat_interval = activity_data.repeat_interval,
                schedule_id = new_schedule.id,
                created_at = datetime.now(),
                updated_at = datetime.now()
            )
            db.add(new_activity)
            db.commit()
            db.refresh(new_activity)

            if activity_data.notifications:
                for notification in activity_data.notifications:
                    new_notification = Notification(
                        message = notification.message,
                        status = notification.status,
                        time = notification.time,
                        user_id = new_schedule.user_id,
                        activity_id = new_activity.id
                    )
                    db.add(new_notification)
                    db.commit()
                    db.refresh(new_notification)


            if activity_data.type == "TASK":
                new_task = Task(
                    name = activity_data.metadata.name,
                    detail = activity_data.metadata.detail,
                    activity_id = new_activity.id,
                    due_time = activity_data.metadata.due_time,
                    created_at = new_activity.created_at,
                    updated_at = new_activity.updated_at
                )
                db.add(new_task)
                db.commit()
                db.refresh(new_task)
            elif activity_data.type == "EVENT":
                new_event = Event(
                    title = activity_data.metadata.title,
                    description = activity_data.metadata.description,
                    activity_id = new_activity.id,
                    start_time = activity_data.metadata.start_time,
                    end_time = activity_data.metadata.end_time,
                    created_at = new_activity.created_at,
                    updated_at = new_activity.updated_at
                )
                db.add(new_event)
                db.commit()
                db.refresh(new_event)

    return {
        "status": "success",
        "message": "New schedule has been created"
    }

@router.put("/{schedule_id}", dependencies=[Depends(verifyAuth)])
def updateSchedule(schedule_id:int, schedule: ScheduleBody, db: Session=Depends(get_db)):
    existing_schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()

    if not existing_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    existing_schedule.name = schedule.name
    existing_schedule.user_id = schedule.user_id
    existing_schedule.color = schedule.color
    existing_schedule.updated_at = datetime.now()

    db.commit()

    updated_schedule = {
        "id": existing_schedule.id,
        "name": existing_schedule.name,
        "user_id": existing_schedule.user_id,
        "color": existing_schedule.color,
        "created_at": existing_schedule.created_at,
        "updated_at": existing_schedule.updated_at
    }

    return {
        "status": "success",
        "data": updated_schedule
    }


@router.post("/generate", dependencies=[Depends(verifyAuth)])
def generateSchedule(prompt: str, db: Session=Depends(get_db)):
    return

@router.delete("/{schedule_id}", dependencies=[Depends(verifyAuth)])
def deleteSchedule(schedule_id: int, db: Session=Depends(get_db)):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Data not found")
    
    db.delete(schedule)
    db.commit()

    return {
        "status": "success",
        "message": "Deleted successfully"
    }

@router.get("/", dependencies=[Depends(verifyAuth)])
def getAllSchedules(db: Session=Depends(get_db)):
    schedules = db.query(Schedule).all()

    return {
        "status": "success",
        "data": schedules
    }

@router.get("/{schedule_id}", dependencies=[Depends(verifyAuth)])
def getScheduleDetail(schedule_id: int, db: Session=Depends(get_db)):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Data not found")
    
    tasks = db.query(Task, Activity).join(Activity).filter(Activity.schedule_id == schedule.id).all()
    events = db.query(Event, Activity).join(Activity).filter(Activity.schedule_id == schedule.id).all()

        # Fetch notifications related to the schedule's activities
    task_activities = []
    for task, activity in tasks:
        notifications = db.query(Notification).filter(Notification.activity_id == activity.id).all()
        notification_data = [{
            "id": notification.id,
            "message": notification.message,
            "status": notification.status,
            "time": notification.time,
            "created_at": notification.created_at,
            "updated_at": notification.updated_at
        } for notification in notifications]

        task_activities.append({
            "date": activity.date,
            "repeat_interval": activity.repeat_interval,
            "type": 'TASK',
            "metadata": {
                "id": task.id,
                "name": task.name,
                "detail": task.detail,
                "due_time": task.due_time,
                "created_at": task.created_at,
                "updated_at": task.updated_at
            },
            "notifications": notification_data
        })

    event_activities = []
    for event, activity in events:
        notifications = db.query(Notification).filter(Notification.activity_id == activity.id).all()
        notification_data = [{
            "id": notification.id,
            "message": notification.message,
            "status": notification.status,
            "time": notification.time,
            "created_at": notification.created_at,
            "updated_at": notification.updated_at
        } for notification in notifications]

        event_activities.append({
            "date": activity.date,
            "repeat_interval": activity.repeat_interval,
            "type": 'EVENT',
            "metadata": {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "start_time": event.start_time,
                "end_time": event.end_time,
                "created_at": event.created_at,
                "updated_at": event.updated_at
            },
            "notifications": notification_data
        })

    activities = task_activities + event_activities
    
    return {
        "status": "success",
        "data": {
            "id": schedule.id,
            "name": schedule.name,
            "color": schedule.color,
            "user_id": schedule.user_id,
            "created_at": schedule.created_at,
            "updated_at": schedule.updated_at,
        },
        "activites": activities
    }

@router.get("/user/{user_email}", dependencies=[Depends(verifyAuth)])
def getSchedulesByUser(user_email: str, db: Session=Depends(get_db), search: str = Query(None), sort: str = Query(None), page: int = Query(1, gt=0), limit: int = Query(10, gt=0), detail: bool = Query(None)):
    existing_user = db.query(User).filter(User.email == user_email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="Target user not found")
    
    sort_order = asc if sort == "asc" else desc
    offset = (page - 1) * limit

    base_query = db.query(Schedule).filter(Schedule.user_id == existing_user.id)
    
    if search:
        base_query = base_query.filter(Schedule.name.ilike(f"%{search}%"))

    total_count = base_query.with_entities(func.count(Schedule.id)).scalar()

    total_pages = (total_count + limit - 1) // limit

    retrieved_schedules = base_query.order_by(sort_order(Schedule.created_at)).offset(offset).limit(limit).all()

    if detail:
        schedules_with_details = []
        for schedule in retrieved_schedules:
            tasks = db.query(Task, Activity).join(Activity).filter(Activity.schedule_id == schedule.id).all()
            events = db.query(Event, Activity).join(Activity).filter(Activity.schedule_id == schedule.id).all()

            task_activities = [{
                "date": activity.date,
                "repeat_interval": activity.repeat_interval,
                "type": 'TASK',
                "metadata": {
                    "id": task.id,
                    "name": task.name,
                    "detail": task.detail,
                    "due_time": task.due_time,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at
                }
            } for task, activity in tasks]

            event_activities = [{
                "date": activity.date,
                "repeat_interval": activity.repeat_interval,
                "type": 'EVENT',
                "metadata": {
                    "id": event.id,
                    "title": event.title,
                    "description": event.description,
                    "start_time": event.start_time,
                    "end_time": event.end_time,
                    "created_at": event.created_at,
                    "updated_at": event.updated_at
                }
            } for event, activity in events]

            activities = task_activities + event_activities

            schedules_with_details.append({
                "schedule": schedule,
                "activities": activities
            })

        retrieved_schedules = schedules_with_details
    
    return {
        "status": "success",
        "data": retrieved_schedules,
        "currentPage": page,
        "totalPages": total_pages,
        "totalItems": total_count  
    }