import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import schemas, services
from db import get_db
from sqlalchemy.orm import Session


app = FastAPI()

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

@app.get("/favorites/", response_model=list[schemas.FavoriteBase])
async def get_favorite_movies(user_id: int, db: Session = Depends(get_db)):
    return services.get_favorites(db, user_id)

@app.post("/favorites/", response_model=schemas.FavoriteBase)
async def add_favorites(movie: schemas.FavoriteBase, db: Session = Depends(get_db)):
    return services.set_favorite(db, movie)
    
@app.get("/user/", response_model=list[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    return services.get_users(db)

@app.post("/user/", response_model=schemas.UserBase)
async def add_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    return services.create_user(db, user)

@app.post("/favorites/remove/")
async def remove_favorites(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    return services.remove_favorite(db, user_id, movie_id)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)