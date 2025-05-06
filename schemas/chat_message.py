from pydantic import BaseModel
from datetime import datetime

class ChatMessageCreate(BaseModel):
    meeting_id: str
    sender_id: str
    message: str

class ChatMessageResponse(BaseModel):
    id: str
    meeting_id: str
    sender_id: str
    timestamp: datetime
    message: str

    class Config:
        orm_mode = True
