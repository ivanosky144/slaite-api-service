from pydantic import BaseModel
from typing import List, Union, Optional
from datetime import date, time

class Notification(BaseModel):
    message: str
    status: str
    time: str

class TaskDetail(BaseModel):
    name: str
    detail: str
    due_time: time

class EventDetail(BaseModel):
    title: str
    description: str
    start_time: time
    end_time: time

class ActivityDetail(BaseModel):
    date: date
    repeat_interval: str
    type: str
    metadata: Union[TaskDetail, EventDetail]
    notifications: Optional[List[Notification]]
    

class ScheduleBody(BaseModel):
    name: str
    user_id: int
    activities: List[ActivityDetail]
    color: str