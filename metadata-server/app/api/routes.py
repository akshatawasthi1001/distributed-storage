import os
import shutil

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.file_model import File as FileModel

router = APIRouter()

STORAGE_DIR = "storage"

os.makedirs(STORAGE_DIR, exist_ok=True)


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


@router.get("/files")
def list_files(db: Session = Depends(get_db)):

    files = db.query(FileModel).all()

    return [
        {
            "id": str(file.id),
            "filename": file.filename,
            "size": file.size,
            "storage_path": file.storage_path
        }
        for file in files
    ]

@router.get("/download/{file_id}")
def download_file(
    file_id: str,
    db: Session = Depends(get_db)
):

    file_record = db.query(FileModel).filter(
        FileModel.id == file_id
    ).first()

    if not file_record:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return FileResponse(
        path=file_record.storage_path,
        filename=file_record.filename,
        media_type="application/octet-stream"
    )

@router.delete("/files/{file_id}")
def delete_file(
    file_id: str,
    db: Session = Depends(get_db)
):

    file_record = db.query(FileModel).filter(
        FileModel.id == file_id
    ).first()

    if not file_record:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if os.path.exists(file_record.storage_path):
        os.remove(file_record.storage_path)

    db.delete(file_record)
    db.commit()

    return {
        "message": "File deleted successfully",
        "file_id": file_id
    }
@router.get("/files/{file_id}")
def get_file_metadata(
    file_id: str,
    db: Session = Depends(get_db)
):

    file_record = db.query(FileModel).filter(
        FileModel.id == file_id
    ).first()

    if not file_record:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return {
        "id": str(file_record.id),
        "filename": file_record.filename,
        "size": file_record.size,
        "storage_path": file_record.storage_path
    }