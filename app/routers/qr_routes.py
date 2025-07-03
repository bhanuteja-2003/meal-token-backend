import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.models.user import User
from app.dependencies import get_current_user
router = APIRouter()

@router.get("/{user_id}/{event_id}")
def get_qr_image(user_id: int, event_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and current_user.role == "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view this QR")
    qr_folder = "generated_qrs"
    filename = f"qr_user{user_id}_event{event_id}.png"
    filepath = os.path.join(qr_folder, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="QR code not found")

    return FileResponse(filepath, media_type="image/png", filename=filename)
