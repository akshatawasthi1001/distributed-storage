import os
import shutil

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.file_model import File as FileModel

router = APIRouter()

STORAGE_DIR = "storage"

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    file_path = os.path.join(STORAGE_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_path)

    new_file = FileModel(
        filename=file.filename,
        storage_path=file_path,
        size=file_size
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "file_id": str(new_file.id),
        "filename": new_file.filename,
        "size": new_file.size,
        "saved_at": new_file.storage_path
    }