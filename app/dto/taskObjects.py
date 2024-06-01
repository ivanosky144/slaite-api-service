from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class RepeatInterval(str, Enum):
    Daily = "Daily"
    Weekly = "Weekly"
    Monthly = "Monthly"

class TaskBody(BaseModel):
    date: datetime
    name: str
    detail: str
    user_id: int
    schedule_id: int
    repeat_interval: RepeatInterval
    due_time: datetime
