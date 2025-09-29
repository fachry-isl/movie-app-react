from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Database connection URL (update with actual credentials)
DATABASE_URL = "postgresql://postgres:N%40vyclub321@localhost/movie_db"

# Create engine and base class
engine = create_engine(DATABASE_URL)
Base = declarative_base()


# Create session
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

