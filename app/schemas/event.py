from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    form_deadline: datetime

class EventOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    date: datetime
    form_deadline: datetime
    created_at: datetime

    class Config:
        orm_mode = True
