from pydantic import BaseModel
from datetime import date
from typing import Optional

class CourseCreate(BaseModel):
    code: str
    title: str
    teacher_id: str

class CourseResponse(BaseModel):
    id: str
    title: str
    code: str
    teacher_id: str

    class Config:
        from_attributes = True  # 🔁 Pydantic v2 remplace `orm_mode = True`
