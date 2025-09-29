from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models import Favorite, User
from schemas import FavoriteBase, UserBase


def set_favorite(db: Session, data: FavoriteBase):
    try:
        # Check if movie already exists for any user
        existing_favorite = db.query(Favorite).filter(Favorite.movie_id == data.movie_id).first()
        if existing_favorite:
            raise HTTPException(
                status_code=409,
                detail=f"Movie with ID {data.movie_id} already exists in favorites"
            )
        
        movie_instance = Favorite(**data.model_dump())
        db.add(movie_instance)
        db.commit()
        db.refresh(movie_instance)
        return movie_instance
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Movie with ID {data.movie_id} already exists in favorites"
        )


def get_favorites(db: Session, user_id: int):
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()
    

def create_user(db: Session, data: UserBase):
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
    # Find the specific favorite to delete
    favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id, 
        Favorite.movie_id == movie_id
    ).first()
    
    if not favorite:
        raise HTTPException(
            status_code=404,
            detail="Favorite movie not found for this user"
        )
    
    # Delete the found favorite
    db.delete(favorite)
    db.commit()
    
    # No need to refresh after delete - the object is removed
    return {"message": "Favorite removed successfully"}
