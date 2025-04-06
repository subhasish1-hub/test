from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from database import Base, engine  # Ensure engine is imported from database
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)

    # Relationships
    ratings = relationship("Rating", back_populates="user")
    search_history = relationship("UserSearchHistory", back_populates="user")
    cart_items = relationship("UserCart", back_populates="user")
    orders = relationship("UserOrder", back_populates="user")


class Food(Base):
    __tablename__ = "food"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    category = Column(String)
    is_veg = Column(Boolean)

    # Relationships
    ratings = relationship("Rating", back_populates="food")
    search_history = relationship("UserSearchHistory", back_populates="food")
    cart_items = relationship("UserCart", back_populates="food")
    orders = relationship("UserOrder", back_populates="food")


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("food.id"), nullable=False)
    rating = Column(Float, nullable=False)

    user = relationship("User", back_populates="ratings")
    food = relationship("Food", back_populates="ratings")

    # Ensure that a user can rate a food item only once
    __table_args__ = (UniqueConstraint('user_id', 'food_id', name='unique_user_food'),)

class UserSearchHistory(Base):
    __tablename__ = "user_search_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food_id = Column(Integer, ForeignKey("food.id"))
    searched_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="search_history")
    food = relationship("Food", back_populates="search_history")

class UserCart(Base):
    __tablename__ = "user_cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food_id = Column(Integer, ForeignKey("food.id"))
    quantity = Column(Integer, default=1)
    added_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="cart_items")
    food = relationship("Food", back_populates="cart_items")

class UserOrder(Base):
    __tablename__ = "user_orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food_id = Column(Integer, ForeignKey("food.id"))
    order_count = Column(Integer, default=1)
    last_ordered = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="orders")
    food = relationship("Food", back_populates="orders")

# Ensure tables are created in the database
Base.metadata.create_all(bind=engine)
