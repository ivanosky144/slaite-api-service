from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.taskModel import Task
from models.activityModel import Activity
from models.scheduleModel import Schedule
from models.userModel import User
from dto.taskObjects import TaskBody
from config.database import get_db
from datetime import datetime
from middleware.authentication import verifyAuth

router = APIRouter(tags=["Tasks"])

@router.get("/{task_id}", dependencies=[Depends(verifyAuth)])
def getTaskDetail(task_id: int, db: Session=Depends(get_db)):
    task_detail = db.query(Task).get(task_id)
    if not task_detail:
        raise HTTPException(status_code=404, detail="Task not found")
    
    activity_data = db.query(Activity).get(task_detail.activity_id)

    payload = {
        "name": task_detail.name,
        "detail": task_detail.detail,
        "schedule_id": activity_data.schedule_id,
        "repeat_interval": activity_data.repeat_interval,
        "date": activity_data.date,
        "due_time": task_detail.due_time
    }

    return {
        "status": "success",
        "data": payload
    }

@router.post("/", dependencies=[Depends(verifyAuth)])
def createTask(task: TaskBody, db: Session=Depends(get_db)):

    used_schedule = db.query(Schedule).filter(Schedule.id == task.schedule_id)

    if not used_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    new_activity = Activity(
        date = task.date,
        repeat_interval = task.repeat_interval,
        schedule_id = task.schedule_id,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)

    new_task = Task(
        name = task.name,
        detail = task.detail,
        due_time = task.due_time,
        activity_id = new_activity.id,
        created_at = new_activity.created_at,
        updated_at = new_activity.updated_at
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "status": "success",
        "message": "New task has been created"
    }

@router.get("/user/{user_email}", dependencies=[Depends(verifyAuth)])
def getTasksByUser(user_email: str, db: Session=Depends(get_db), start_date: str = Query(None), end_date: str = Query(None)):
    existing_user = db.query(User).filter(User.email == user_email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="Target user not found")
    
    tasks = db.query(Task, Activity).join(Activity).filter(Activity.schedule.has(user_id=existing_user.id)).all()

    task_activities = [{
        "date": activity.date,
        "repeat_interval": activity.repeat_interval,
        "activity_id": activity.id,
        "id": task.id,
        "name": task.name,
        "due_time": task.due_time,
        "created_at": task.created_at,
        "updated_at": task.updated_at
    } for task, activity in tasks]
    
    return {
        "status": "success",
        "data": task_activities
    }

@router.put("/{event_id}", dependencies=[Depends(verifyAuth)])
def updateTask():
    return

@router.delete("/{event_id}", dependencies=[Depends(verifyAuth)])
def deleteTask():
    return