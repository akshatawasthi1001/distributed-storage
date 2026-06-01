from app.db.database import engine
from app.models.file_model import File

Base = File.metadata

Base.create_all(bind=engine)

print("Database tables created successfully")