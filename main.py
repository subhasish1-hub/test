from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from sqlalchemy import text
from database import get_db, engine, Base
from models import User, Food, Rating, UserSearchHistory, UserCart, UserOrder
import os
from passlib.context import CryptContext
from schemas import FoodRecommendationResponse, FoodRecommendationRequest, FoodSchema
from recommendation import hybrid_recommendation
from sqlalchemy import func
from typing import List

# Ensure tables are created (Temporary Fix)
Base.metadata.create_all(bind=engine)

# Define FastAPI instance before routes
app = FastAPI()

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/")
def root():
    return {"message": "🚀 FastAPI is running!"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    database_url = os.getenv("DATABASE_URL")
    try:
        result = db.execute(text("SELECT 1"))
        return {
            "status": "✅ Database Connected!",
            "result": result.fetchone(),
            "DATABASE_URL": database_url
        }
    except Exception as e:
        return {
            "status": "❌ Database Connection Failed",
            "error": str(e),
            "DATABASE_URL": database_url
        }

# Corrected recommend Endpoint
@app.post("/recommend-food", response_model=FoodRecommendationResponse)
def recommend_food(request: FoodRecommendationRequest, db: Session = Depends(get_db)):
    recommendations = hybrid_recommendation(request.user_id, request.liked_food, request.veg_only)

    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found for this user.")

    # Fetch Food objects from the database based on the returned food names
    recommended_foods = db.query(Food).filter(Food.name.in_(recommendations)).all()

    return {"recommended_foods": recommended_foods}