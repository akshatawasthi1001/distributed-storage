from app.db.database import engine
from app.models.file_model import File
from app.models.file_version_model import FileVersion

# Create all tables
File.metadata.create_all(bind=engine)

print("Database tables created successfully")