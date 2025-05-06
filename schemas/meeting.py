from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class MeetingStatus(str, Enum):
    scheduled = "scheduled"
    live = "live"
    completed = "completed"

class MeetingCreate(BaseModel):
    course_id: str
    start_time: datetime
    end_time: datetime
    join_url: str
    status: MeetingStatus = MeetingStatus.scheduled

class MeetingResponse(BaseModel):
    id: str
    course_id: str
    start_time: datetime
    end_time: datetime
    join_url: str
    status: MeetingStatus

    class Config:
        orm_mode = True
