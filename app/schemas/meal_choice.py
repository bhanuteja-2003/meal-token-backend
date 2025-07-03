from pydantic import BaseModel, constr
from typing import Literal

class MealChoiceCreate(BaseModel):
    event_id: int
    choice: Literal["veg", "non-veg"]

class MealChoiceOut(BaseModel):
    event_id: int
    user_id: int
    choice: str

    class Config:
        orm_mode = True
