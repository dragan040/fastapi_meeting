from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from database import Base
import uuid
import enum

class RoleEnum(str, enum.Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)

    courses = relationship("Course", back_populates="teacher", cascade="all, delete-orphan")

    # Relation avec les messages envoyés (chat)
    messages_sent = relationship("ChatMessage", back_populates="sender", foreign_keys="ChatMessage.sender_id")
