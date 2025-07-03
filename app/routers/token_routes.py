from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.token import Token
from app.dependencies import get_db

router = APIRouter()

@router.post("/validate/{token_uuid}")
def validate_token(token_uuid: str, db: Session = Depends(get_db)):
    token = db.query(Token).filter(Token.token_uuid == token_uuid).first()

    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    if token.is_used:
        raise HTTPException(status_code=400, detail="Token already used")

    # Mark as used
    token.is_used = True
    db.commit()

    return {
        "status": "Token valid and marked as used",
        "user_id": token.user_id,
        "event_id": token.event_id,
        "meal_choice": token.meal_choice
    }

# testing purpose only :
@router.get("/validate/{token_uuid}")
def test_validate_token(token_uuid: str, db: Session = Depends(get_db)):
    token = db.query(Token).filter(Token.token_uuid == token_uuid).first()

    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    if token.is_used:
        raise HTTPException(status_code=400, detail="Token already used")

    # Mark as used
    token.is_used = True
    db.commit()

    return {
        "status": "Token valid and marked as used",
        "user_id": token.user_id,
        "event_id": token.event_id,
        "meal_choice": token.meal_choice
    }