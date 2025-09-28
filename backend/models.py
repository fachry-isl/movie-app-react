from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from db import Base

# Define User table
class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    favorites = relationship("Favorite", back_populates="user")

# Define Favorites table
class Favorite(Base):
    __tablename__ = "favorites"
    favorite_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    movie_id = Column(Integer, nullable=False)
    movie_name = Column(String, nullable=False)
    movie_description = Column(String)
    user = relationship("User", back_populates="favorites")