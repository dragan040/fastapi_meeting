from sqlalchemy.orm import Session
from models.chat_message import ChatMessage
from schemas.chat_message import ChatMessageCreate

def create_message(db: Session, message: ChatMessageCreate):
    db_message = ChatMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_by_meeting(db: Session, meeting_id: str):
    return db.query(ChatMessage).filter(ChatMessage.meeting_id == meeting_id).order_by(ChatMessage.timestamp).all()
