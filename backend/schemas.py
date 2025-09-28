from pydantic import BaseModel

class FavoriteBase(BaseModel):
    user_id: int
    movie_id: int
    movie_name: str
    movie_description: str | None = None

class FavoriteOut(FavoriteBase):
    favorite_id: int
    user_id: int

    class Config:
        from_attribute = True

class UserBase(BaseModel):
    username: str
    password: str

class UserOut(UserBase):
    user_id: int
    favorites: list[FavoriteOut] = []
    

    class Config:
        from_attribute = True