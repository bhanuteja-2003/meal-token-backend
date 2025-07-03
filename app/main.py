from fastapi import FastAPI
from app.routers import user_routes, event_routes, meal_choice_routes, token_routes, qr_routes
from app.core.database import Base, engine


# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(event_routes.router, prefix="/events", tags=["Events"])
app.include_router(meal_choice_routes.router, prefix="/meal-choice", tags=["Meal Choice"])
app.include_router(token_routes.router, prefix="/tokens", tags=["Tokens"])
app.include_router(qr_routes.router, prefix="/qr", tags=["QR"])

