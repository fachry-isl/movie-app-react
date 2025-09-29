from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models import Favorite, User, Movie
from schemas import FavoriteBase, UserBase


def set_favorite(db: Session, data: FavoriteBase, user_id: int):
    """
    Add a favorite movie for a user.
    If the movie doesn't exist in Movie table, create it first.
    Prevents duplicate favorites per user.
    """

    # 1. Ensure the movie exists in Movie table
    movie = db.query(Movie).filter(Movie.movie_id == data.movie_id).first()
    if not movie:
        movie = Movie(
            movie_id=data.movie_id,
            movie_name=data.movie_name,
            movie_description=data.movie_description
        )
        db.add(movie)
        db.commit()
        db.refresh(movie)

    # 2. Check if this user already favorited the movie
    existing_favorite = (
        db.query(Favorite)
        .filter(Favorite.user_id == user_id, Favorite.movie_id == data.movie_id)
        .first()
    )
    if existing_favorite:
        raise HTTPException(
            status_code=409,
            detail=f"User {user_id} already favorited movie {data.movie_id}"
        )

    # 3. Add the favorite relationship
    favorite = Favorite(user_id=user_id, movie_id=data.movie_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return favorite


def get_favorites(db: Session, user_id: int):
    """
    Get all favorite movies for a user, with movie details.
    """
    return (
        db.query(Favorite)
        .filter(Favorite.user_id == user_id)
        .join(Movie, Favorite.movie_id == Movie.movie_id)
        .all()
    )


def create_user(db: Session, data: UserBase):
    """
    Create a new user.
    """
    try:
        user_instance = User(**data.model_dump())
        db.add(user_instance)
        db.commit()
        db.refresh(user_instance)
        return user_instance
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )


def get_users(db: Session):
    return db.query(User).all()


def remove_favorite(db: Session, user_id: int, movie_id: int):
    """
    Remove a specific favorite movie for a user.
    """
    favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.movie_id == movie_id
    ).first()

    if not favorite:
        raise HTTPException(
            status_code=404,
            detail="Favorite movie not found for this user"
        )

    db.delete(favorite)
    db.commit()
    return {"message": "Favorite removed successfully"}
