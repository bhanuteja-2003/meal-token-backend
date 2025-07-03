from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class MealChoice(Base):
    __tablename__ = "meal_choices"
    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    
    choice = Column(String, nullable=False)  # "veg" or "non-veg"

    __table_args__ = (UniqueConstraint('user_id', 'event_id', name='_user_event_uc'),)

    # Optional: relationships if you want joins later
    user = relationship("User")
    event = relationship("Event")
