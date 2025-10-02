from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid


# Define User table
class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    User model that uses UUID as primary key.
    SQLAlchemyBaseUserTableUUID already provides:
    - id: UUID column (primary key)
    - email: String column
    - hashed_password: String column
    - is_active: Boolean column
    - is_superuser: Boolean column
    - is_verified: Boolean column
    """
    __tablename__ = "user"
    
    # One user can have many favorites
    # Note: The foreign key in Favorite table should reference 'user.id' not 'user.user_id'
    favorites = relationship("Favorite", back_populates="user")


# Define Movie table (new, to achieve 3NF)
class Movie(Base):
    __tablename__ = "movie"

    movie_id = Column(Integer, primary_key=True, index=True)  # from TMDB API
    title = Column(String, nullable=False)
    overview = Column(String)
    
    # New Field
    release_date = Column(String)
    poster_path = Column(String)
    vote_average = Column(Float)
    vote_count = Column(Integer)
    genres = Column(ARRAY(Integer))
    popularity = Column(Float)
    original_language = Column(String)

    # One movie can be favorited by many users
    favorites = relationship("Favorite", back_populates="movie")


# Define Favorites table (join table for User and Movie)
class Favorite(Base):
    __tablename__ = "favorites"

    favorite_id = Column(Integer, primary_key=True, index=True)
    # Changed: Reference 'user.id' instead of 'user.user_id'
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movie.movie_id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="favorites")
    movie = relationship("Movie", back_populates="favorites")

    # Prevent duplicate favorites for same user + movie
    __table_args__ = (UniqueConstraint("user_id", "movie_id", name="_user_movie_uc"),)