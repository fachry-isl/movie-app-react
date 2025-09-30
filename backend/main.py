import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
import services
from db import get_async_session, create_db_and_tables
from models import User
from users import auth_backend, fastapi_users, current_active_user

app = FastAPI()

# Enable CORS if frontend is separate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourfrontend.com"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include FastAPI Users routers
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(schemas.UserRead, schemas.UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(schemas.UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(schemas.UserRead, schemas.UserUpdate),
    prefix="/users",
    tags=["users"],
)

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    """Example protected route"""
    return {"message": f"Hello {user.email}!"}

# =========================
# Favorites Endpoints
# =========================

@app.get("/favorites/", response_model=list[schemas.FavoriteOut], tags=["favorites"])
async def get_favorite_movies(
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Get all favorite movies for the authenticated user"""
    return await services.get_favorites(db, user.id)

@app.post("/favorites/", response_model=schemas.FavoriteOut, tags=["favorites"])
async def add_favorites(
    movie: schemas.MovieBase,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Add a favorite movie for the authenticated user.
    - If movie doesn't exist → create in Movie table.
    - Then create entry in Favorite table.
    """
    return await services.set_favorite(db, movie, user.id)

@app.delete("/favorites/", tags=["favorites"])
async def remove_favorites(
    movie_id: int,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Remove a favorite movie for the authenticated user"""
    return await services.remove_favorite(db, user.id, movie_id)

# =========================
# Legacy User Endpoints (Optional - for backward compatibility)
# Note: Use /users/me from fastapi-users instead
# =========================

@app.get("/user/")
async def get_users_legacy(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    """
    Legacy endpoint - Use GET /users/me instead
    This endpoint requires authentication and only returns current user info
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "is_active": current_user.is_active
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)