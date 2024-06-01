from pydantic import BaseModel
from datetime import datetime

class NotificationBody(BaseModel):
    message: str
    status: str
    time: datetime
    user_id: int
    activity_id: int