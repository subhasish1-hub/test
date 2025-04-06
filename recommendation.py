import pandas as pd
import numpy as np
import string
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.neighbors import NearestNeighbors
from schemas import FoodRecommendationRequest
import logging

app = FastAPI()

# Database Connection
DATABASE_URL = "postgresql://postgres:Iita202601@localhost:5432/fastapi_db"
engine = create_engine(DATABASE_URL)

# Load Data from PostgreSQL
food_df = pd.read_sql("SELECT id, name, description, category, is_veg FROM food", con=engine)
ratings_df = pd.read_sql("SELECT user_id, food_id, rating FROM ratings", con=engine)
orders_df = pd.read_sql("SELECT user_id, food_id FROM user_orders", con=engine)

# Merge DataFrames
df = food_df.copy()
df.rename(columns={'name': 'Name', 'description': 'Describe', 'is_veg': 'is_veg'}, inplace=True)

# Data Preprocessing: Text Cleaning
def text_cleaning(text):
    return "".join([char for char in text if char not in string.punctuation])

df['Describe'] = df['Describe'].apply(text_cleaning)

# TF-IDF for Content-Based Filtering
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Describe'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Create Food Index for Searching
indices = pd.Series(df.index, index=df['Name']).drop_duplicates()

# Content-Based Recommendation Function
def get_recommendations(food_name, veg_only=None):
    if food_name not in indices:
        return []

    idx = indices[food_name]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Top 5 similar foods

    food_indices = [i[0] for i in sim_scores]
    recommendations = df.iloc[food_indices]

    if veg_only is not None:
        recommendations = recommendations[recommendations['is_veg'] == veg_only]

    return recommendations['Name'].tolist()

# Collaborative Filtering using Nearest Neighbors
user_matrix = orders_df.pivot_table(index='user_id', columns='food_id', aggfunc=len, fill_value=0)

# Train KNN Model
model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
model_knn.fit(user_matrix)

# Hybrid Recommendation (Content + Collaborative)
import logging

def hybrid_recommendation(user_id, liked_food, veg_only=None):
    logging.info(f"hybrid_recommendation called with: user_id={user_id}, liked_food='{liked_food}', veg_only={veg_only}")
    try:
        content_recommendations = get_recommendations(liked_food, veg_only)

        if user_id in user_matrix.index:
            user_vec = user_matrix.loc[user_id].values.reshape(1, -1)
            distances, indices = model_knn.kneighbors(user_vec, n_neighbors=2)

            similar_users = user_matrix.iloc[indices[0]]
            collaborative_recommendations = similar_users.mean().sort_values(ascending=False).index[:5].tolist()

            recommended_food = food_df[food_df['id'].isin(collaborative_recommendations)]
            combined_recommendations = list(set(content_recommendations) | set(recommended_food['name'].tolist()))

            # Apply veg_only filter after combining recommendations
            if veg_only is not None:
                combined_recommendations = [food for food in combined_recommendations if food in df[df['is_veg'] == veg_only]['Name'].tolist()]

            return combined_recommendations

        return content_recommendations

    except Exception as e:
        logging.error(f"Error in hybrid_recommendation: {e}")
        raise  # Re-raise the exception to trigger 500 error

# FastAPI Endpoint
@app.post("/recommend-food")
def recommend_food(request: FoodRecommendationRequest):
    recommendations = hybrid_recommendation(request.user_id, request.liked_food, request.veg_only)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")
    return {"recommendations": recommendations}

# Test the recommendation function before using FastAPI
print(hybrid_recommendation(1, "Panner Butter Masala", True))
