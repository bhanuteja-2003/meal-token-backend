from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime


from app.models.meal_choice import MealChoice
from app.models.event import Event
from app.schemas.meal_choice import MealChoiceCreate, MealChoiceOut
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.token import Token
from app.utils.qr_generator import generate_token_and_qr

router = APIRouter()

@router.post("/", response_model=MealChoiceOut)
def submit_meal_choice(data: MealChoiceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if event exists
    event = db.query(Event).filter(Event.id == data.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check deadline
    if datetime.utcnow() > event.form_deadline:
        raise HTTPException(status_code=403, detail="Deadline has passed")

    # Check if already submitted
    existing = db.query(MealChoice).filter_by(user_id=current_user.id, event_id=data.event_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already submitted choice for this event")

    # Submit choice
    choice = MealChoice(user_id=current_user.id, event_id=data.event_id, choice=data.choice)
    db.add(choice)
    db.commit()
    db.refresh(choice)


    # Check if token already exists (shouldn't, just in case)
    existing_token = db.query(Token).filter_by(user_id=current_user.id, event_id=data.event_id).first()
    if existing_token:
        raise HTTPException(status_code=400, detail="Token already generated")

    # Generate QR token
    token_uuid, _ = generate_token_and_qr(current_user.id, data.event_id)

    # Save token
    token = Token(
        user_id=current_user.id,
        event_id=data.event_id,
        meal_choice=data.choice,
        token_uuid=token_uuid,
        is_used=False
    )
    db.add(token)
    db.commit()
    return choice

@router.get("/my-choice/{event_id}", response_model=MealChoiceOut)
def get_my_choice(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    choice = db.query(MealChoice).filter_by(user_id=current_user.id, event_id=event_id).first()
    if not choice:
        raise HTTPException(status_code=404, detail="No choice submitted yet")
    return choice

@router.get("/summary/{event_id}")
def get_event_summary(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can view summary")

    veg_count = db.query(MealChoice).filter_by(event_id=event_id, choice="veg").count()
    non_veg_count = db.query(MealChoice).filter_by(event_id=event_id, choice="non-veg").count()

    return {"veg": veg_count, "non_veg": non_veg_count}
