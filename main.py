from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import base64
import json
from models import user, course, meeting  # ✅ assure-toi que `meeting` est bien là
from fastapi import Path
from schemas.meeting import MeetingStatus
import schemas
from schemas.meeting import MeetingResponse

# 📦 Imports internes
from database import SessionLocal, engine, Base
from models import user
from schemas.user import UserCreate, UserResponse
from crud import user as crud_user

from models import course
from schemas.course import CourseCreate, CourseResponse
from crud import course as crud_course

from models import meeting
from schemas.meeting import MeetingCreate, MeetingResponse
from crud import meeting as crud_meeting

from models import chat_message
from schemas.chat_message import ChatMessageCreate, ChatMessageResponse
from crud import chat_message as crud_chat
from models import user, course, meeting, chat_message

# 🚀 Initialisation de l'app
app = FastAPI()

# 🎯 CORS pour Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Création des tables SQL
Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

# 🔁 Dépendance pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🌐 API : Créer un utilisateur
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé.")
    return crud_user.create_user(db, user)

# 🌐 API : Lister tous les utilisateurs
@app.get("/users/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

# 🌐 API : Créer un cours
@app.post("/courses/", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = crud_course.get_course_by_code(db, course.code)
    if db_course:
        raise HTTPException(status_code=400, detail="Code du cours déjà utilisé.")
    return crud_course.create_course(db, course)

# 🌐 API : Lister tous les cours
@app.get("/courses/", response_model=list[CourseResponse])
def read_courses(db: Session = Depends(get_db)):
    return crud_course.get_courses(db)

# 🌐 API : Supprimer un cours
@app.delete("/courses/{course_id}")
def delete_course(course_id: str, db: Session = Depends(get_db)):
    success = crud_course.delete_course(db, course_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cours introuvable")
    return {"message": "Cours supprimé avec succès"}

# 🌐 API : Créer une réunion
@app.post("/meetings/", response_model=MeetingResponse)
def create_meeting(meeting: MeetingCreate, db: Session = Depends(get_db)):
    return crud_meeting.create_meeting(db, meeting)

# 🌐 API : Lister toutes les réunions
@app.get("/meetings/", response_model=list[MeetingResponse])
def read_meetings(db: Session = Depends(get_db)):
    return crud_meeting.get_meetings(db)

@app.put("/meetings/{meeting_id}/status", response_model=MeetingResponse)
def update_meeting_status(meeting_id: str, status: MeetingStatus, db: Session = Depends(get_db)):
    updated_meeting = crud_meeting.set_status(db, meeting_id, status)
    if updated_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return updated_meeting

# 🌐 API : Supprimer une réunion
@app.delete("/meetings/{meeting_id}")
def delete_meeting(meeting_id: str, db: Session = Depends(get_db)):
    success = crud_meeting.delete_meeting(db, meeting_id)
    if not success:
        raise HTTPException(status_code=404, detail="Réunion introuvable")
    return {"message": "Réunion supprimée avec succès"}

# 🌐 API : Créer un message de chat
@app.post("/messages/", response_model=ChatMessageResponse)
def send_message(message: ChatMessageCreate, db: Session = Depends(get_db)):
    return crud_chat.create_message(db, message)

# 🌐 API : Récupérer tous les messages d'une réunion
@app.get("/messages/{meeting_id}", response_model=list[ChatMessageResponse])
def get_messages(meeting_id: str, db: Session = Depends(get_db)):
    return crud_chat.get_messages_by_meeting(db, meeting_id)


# 📦 Chargement du modèle d'engagement
MODEL_PATH = "models/engagement_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)
CLASS_NAMES = ["Engaged", "Disengaged", "Confused"]

# 🔧 Prétraitement d'image base64
def preprocess_image(b64: str):
    header, _, data = b64.partition(",")
    img_data = base64.b64decode(data or b64)
    img = Image.open(io.BytesIO(img_data)).convert("RGB")
    img = img.resize((128, 128))
    arr = np.array(img) / 255.0
    return np.expand_dims(arr, 0)

# 🔌 WebSocket : prédiction d'engagement en temps réel
@app.websocket("/ws/predict")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            msg = await ws.receive_text()
            payload = json.loads(msg)
            b64img = payload.get("image")
            student_idx = payload.get("studentIndex")

            x = preprocess_image(b64img)
            preds = model.predict(x)[0]
            idx = int(np.argmax(preds))
            label = CLASS_NAMES[idx]
            confidence = float(preds[idx])

            await ws.send_text(json.dumps({
                "timestamp":     payload.get("timestamp"),
                "studentIndex":  student_idx,
                "label":         label,
                "confidence":    confidence
            }))
    except WebSocketDisconnect:
        print("Client déconnecté")
