from db import engine, Base
import models  # ensure models are imported so Base knows them

print("Tables registered:", Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)