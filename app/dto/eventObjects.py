from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class RepeatInterval(str, Enum):
    Daily = "Daily"
    Weekly = "Weekly"
    Monthly = "Monthly"

class EventBody(BaseModel):
    date: datetime
    title: str
    description: str
    user_id: int
    schedule_id: int
    repeat_interval: RepeatInterval
    start_time: datetime
    end_time: datetime
