import time

from fastapi import FastAPI
from sqlalchemy.exc import OperationalError

from app.api.routes import router
from app.api.auth import router as auth_router
from app.db.database import Base, engine

# Import models so SQLAlchemy knows about all tables
from app.models.file_model import File
from app.models.file_version_model import FileVersion

app = FastAPI()


@app.on_event("startup")
def startup():
    for attempt in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database tables created successfully")
            break
        except OperationalError:
            print(f"Database not ready... retry {attempt + 1}/10")
            time.sleep(2)

app.include_router(router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Metadata Server Running"}