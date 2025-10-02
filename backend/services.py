from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from models import Favorite, User, Movie
from schemas import MovieBase

async def set_favorite(db: AsyncSession, data: MovieBase, user_id: int):
    """
    Add a favorite movie for a user.
    If the movie doesn't exist in Movie table, create it first.
    Prevents duplicate favorites per user.
    """
    # 1. Ensure the movie exists in Movie table
    result = await db.execute(select(Movie).filter(Movie.movie_id == data.movie_id))
    movie = result.scalar_one_or_none()
    
    if not movie:
        movie = Movie(
            movie_id=data.movie_id,
            title=data.title,
            overview=data.overview,
            
            release_date=data.release_date,
            poster_path=data.poster_path,
            vote_average=data.vote_average,
            vote_count=data.vote_count,
            genres=data.genres,
            popularity=data.popularity,
            original_language=data.original_language
        )
        db.add(movie)
        await db.commit()
        await db.refresh(movie)

    # 2. Check if this user already favorited the movie
    result = await db.execute(
        select(Favorite).filter(
            Favorite.user_id == user_id, 
            Favorite.movie_id == data.movie_id
        )
    )
    existing_favorite = result.scalar_one_or_none()
    
    if existing_favorite:
        raise HTTPException(
            status_code=409,
            detail=f"User {user_id} already favorited movie {data.movie_id}"
        )

    # 3. Add the favorite relationship
    favorite = Favorite(user_id=user_id, movie_id=data.movie_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite, ["movie"])  # Refresh with movie relationship loaded

    return favorite

async def get_favorites(db: AsyncSession, user_id: int):
    """
    Get all favorite movies for a user, with movie details.
    """
    result = await db.execute(
        select(Favorite)
        .options(selectinload(Favorite.movie))  # Eager load movie data
        .filter(Favorite.user_id == user_id)
    )
    return result.scalars().all()

async def remove_favorite(db: AsyncSession, user_id: int, movie_id: int):
    """
    Remove a specific favorite movie for a user.
    """
    result = await db.execute(
        select(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.movie_id == movie_id
        )
    )
    favorite = result.scalar_one_or_none()

    if not favorite:
        raise HTTPException(
            status_code=404,
            detail="Favorite movie not found for this user"
        )

    await db.delete(favorite)
    await db.commit()
    return {"message": "Favorite removed successfully"}