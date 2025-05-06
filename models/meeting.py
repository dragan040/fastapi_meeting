from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import uuid
import enum

class MeetingStatusEnum(str, enum.Enum):
    scheduled = "scheduled"
    live = "live"
    completed = "completed"

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    join_url = Column(String(255), nullable=False)
    status = Column(Enum(MeetingStatusEnum), nullable=False, default=MeetingStatusEnum.scheduled)

    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="meetings")

    messages = relationship("ChatMessage", back_populates="meeting", cascade="all, delete-orphan")
