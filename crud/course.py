from datetime import datetime
from sqlalchemy.orm import Session
from models.meeting import Meeting
from schemas.meeting import MeetingCreate
from models.course import Course  # adapte si besoin
from schemas.course import CourseCreate  # adapte selon ton projet

def create_meeting(db: Session, meeting: MeetingCreate):
    db_meeting = Meeting(**meeting.dict())
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting
def get_courses(db: Session):
    return db.query(Course).all()

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
def get_course_by_code(db: Session, code: str):
    return db.query(Course).filter(Course.code == code).first()

def get_course_by_code(db: Session, code: str):
    return db.query(Course).filter(Course.code == code).first()

def get_courses(db: Session):
    return db.query(Course).all()

def create_course(db: Session, course: CourseCreate):
    db_course = Course(
        code=course.code,
        title=course.title,
        teacher_id=course.teacher_id ,

    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course