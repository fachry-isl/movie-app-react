import asyncio
from db import create_db_and_tables
import models  # Import models to register them with Base

async def init_database():
    print("Creating database tables...")
    print("Registered tables:", models.Base.metadata.tables.keys())
    await create_db_and_tables()
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_database())