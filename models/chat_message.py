from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import uuid

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False)
    sender_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    meeting_id = Column(String(36), ForeignKey("meetings.id"), nullable=False)
    message = Column(String(500), nullable=False)

    sender = relationship("User", back_populates="messages_sent", foreign_keys=[sender_id])
    meeting = relationship("Meeting", back_populates="messages")
