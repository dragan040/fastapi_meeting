from sqlalchemy.orm import Session
from models.meeting import Meeting
from schemas.meeting import MeetingCreate
from sqlalchemy.orm import Session
from models.meeting import Meeting
from schemas.meeting import MeetingStatus

def set_status(db: Session, meeting_id: str, new_status: MeetingStatus):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        return None
    meeting.status = new_status
    db.commit()
    db.refresh(meeting)
    return meeting

def create_meeting(db: Session, meeting: MeetingCreate):
    db_meeting = Meeting(**meeting.dict())
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

def get_meetings(db: Session):
    return db.query(Meeting).all()

def get_meeting_by_id(db: Session, meeting_id: str):
    return db.query(Meeting).filter(Meeting.id == meeting_id).first()

def delete_meeting(db: Session, meeting_id: str):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if meeting:
        db.delete(meeting)
        db.commit()
        return True
    return False
