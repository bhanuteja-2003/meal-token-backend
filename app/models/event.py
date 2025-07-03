from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    date = Column(DateTime, nullable=False)
    form_deadline = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
