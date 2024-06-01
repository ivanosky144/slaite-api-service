from pydantic import BaseModel

class ActivityBody(BaseModel):
    name: str
    user_id: int