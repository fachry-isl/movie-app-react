import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import schemas, services
from db import get_db
from sqlalchemy.orm import Session

app = FastAPI()

# Enable CORS if frontend is separate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourfrontend.com"],  
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/hello")
async def hello():
    return {"message": "Hello World"}


# =========================
# Favorites Endpoints
# =========================
@app.get("/favorites/", response_model=list[schemas.FavoriteOut])
async def get_favorite_movies(user_id: int, db: Session = Depends(get_db)):
    return services.get_favorites(db, user_id)


@app.post("/favorites/", response_model=schemas.FavoriteOut)
async def add_favorites(
    movie: schemas.MovieBase, user_id: int, db: Session = Depends(get_db)
):
    """
    Add a favorite movie for a user.
    - If movie doesn't exist → create in Movie table.
    - Then create entry in Favorite table.
    """
    return services.set_favorite(db, movie, user_id)


@app.post("/favorites/remove/")
async def remove_favorites(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    return services.remove_favorite(db, user_id, movie_id)


# =========================
# User Endpoints
# =========================
@app.get("/user/", response_model=list[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    return services.get_users(db)


@app.post("/user/", response_model=schemas.UserOut)
async def add_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    return services.create_user(db, user)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
