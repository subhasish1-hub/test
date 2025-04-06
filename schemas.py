from pydantic import BaseModel
from typing import Optional, List

# ✅ Define a schema for Food (modify fields based on your Food model)
class FoodSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True  # Ensures SQLAlchemy models can be converted

# ✅ Fix request schema name
class FoodRecommendationRequest(BaseModel):
    user_id: int
    liked_food: Optional[str] = None
    veg_only: Optional[bool] = None  # Optional: Filter vegetarian-only food

# ✅ Fix response schema name and structure
class FoodRecommendationResponse(BaseModel):
    recommended_foods: List[FoodSchema]
