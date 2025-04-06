from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv  # ✅ Load env variables

# ✅ Load environment variables from .env file
load_dotenv(".env")

# Override DATABASE_URL if it is set to the local database
# if os.getenv("DATABASE_URL") == "postgresql://postgres:Iita202601@localhost:5432/fastapi_db":
#     os.environ["DATABASE_URL"] = "postgresql://avnadmin:AVNS_ONx9vmBRGhXjUyLaJSU@pg-3240166f-food-recommendation.i.aivencloud.com:17426/defaultdb?sslmode=require"

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Using DATABASE_URL: {DATABASE_URL}")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing. Check your .env file!")

# ✅ Create database engine with pool_pre_ping
engine = create_engine(DATABASE_URL, pool_pre_ping=True,echo=True)

# ✅ Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Define Base for models
Base = declarative_base()

# ✅ Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()