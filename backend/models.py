from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db import Base

# Define User table
class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    # One user can have many favorites
    favorites = relationship("Favorite", back_populates="user")


# Define Movie table (new, to achieve 3NF)
class Movie(Base):
    __tablename__ = "movie"

    movie_id = Column(Integer, primary_key=True, index=True)  # from TMDB API
    movie_name = Column(String, nullable=False)
    movie_description = Column(String)

    # One movie can be favorited by many users
    favorites = relationship("Favorite", back_populates="movie")


# Define Favorites table (join table for User and Movie)
class Favorite(Base):
    __tablename__ = "favorites"

    favorite_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movie.movie_id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="favorites")
    movie = relationship("Movie", back_populates="favorites")

    # Prevent duplicate favorites for same user + movie
    __table_args__ = (UniqueConstraint("user_id", "movie_id", name="_user_movie_uc"),)
