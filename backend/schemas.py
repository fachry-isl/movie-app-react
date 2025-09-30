from pydantic import BaseModel
from typing import Optional, List
from fastapi_users import schemas
import uuid

# =========================
# Movie Schemas
# =========================
class MovieBase(BaseModel):
    movie_id: int
    movie_name: str
    movie_description: Optional[str] = None


class MovieOut(MovieBase):
    class Config:
        from_attributes = True


# =========================
# Favorite Schemas
# =========================
class FavoriteBase(BaseModel):
    movie_id: int  # only needs movie_id (Movie table handles details)


class FavoriteOut(BaseModel):
    favorite_id: int
    movie: MovieOut  # nested movie details

    class Config:
        from_attributes = True


# =========================
# User Schemas
# =========================
# class UserBase(BaseModel):
#     username: str
#     password: str


# class UserOut(UserBase):
#     user_id: int
#     favorites: List[FavoriteOut] = []

#     class Config:
#         from_attributes = True
class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass