from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from app.core.database import Base
from sqlalchemy.orm import relationship

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    meal_choice = Column(String, nullable=False)  # "veg" or "non-veg"
    token_uuid = Column(String, unique=True, index=True, nullable=False)
    is_used = Column(Boolean, default=False)

    user = relationship("User")
    event = relationship("Event")

    __table_args__ = (UniqueConstraint('user_id', 'event_id', name='_user_event_token_uc'),)
