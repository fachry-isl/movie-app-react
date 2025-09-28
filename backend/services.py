from sqlalchemy.orm import Session
from models import Favorite, User
from schemas import FavoriteBase, UserBase

def set_favorite(db: Session, data: FavoriteBase):
    movie_instance = Favorite(**data.model_dump())
    db.add(movie_instance)
    db.commit()
    db.refresh(movie_instance)
    return movie_instance

def get_favorites(db: Session, user_id: int):
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()
    
    
def create_user(db: Session, data: UserBase):
    user_instance = User(**data.model_dump())
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)
    return user_instance

def get_users(db: Session):
    return db.query(User).all()