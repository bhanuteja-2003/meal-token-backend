from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.event import EventCreate, EventOut
from app.models.event import Event
from app.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=EventOut)
def create_event(event_data: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create events")
    
    event = Event(**event_data.dict())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("/", response_model=list[EventOut])
def get_all_events(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.date.asc()).all()

@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
