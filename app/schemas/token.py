from pydantic import BaseModel

class TokenOut(BaseModel):
    event_id: int
    user_id: int
    meal_choice: str
    token_uuid: str
    is_used: bool

    class Config:
        orm_mode = True
