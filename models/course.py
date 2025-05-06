from sqlalchemy import Column, DateTime, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Course(Base):
    __tablename__ = "courses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # UUID
    title = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)

    teacher_id = Column(String(36), ForeignKey("users.id"), nullable=False)

    teacher = relationship("User", back_populates="courses")
    meetings = relationship("Meeting", back_populates="course", cascade="all, delete-orphan")
