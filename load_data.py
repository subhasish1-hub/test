import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set in environment variables.")

# Create database engine
engine = create_engine(DATABASE_URL)  # No need to set `sslmode` again

# Load Data from PostgreSQL
try:
    with engine.connect() as conn:
        food_df = pd.read_sql("SELECT id, name, description FROM food", con=conn)
        ratings_df = pd.read_sql("SELECT user_id, food_id, rating FROM ratings", con=conn)
        orders_df = pd.read_sql("SELECT user_id, food_id FROM user_orders", con=conn)

    print("✅ Data Loaded Successfully!")
    print(food_df.head())

except Exception as e:
    print("❌ Database Error:", e)
