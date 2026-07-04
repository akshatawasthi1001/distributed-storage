import os
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
    Query
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.file_model import File as FileModel
from app.models.file_version_model import FileVersion

router = APIRouter()

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)


# ===========================
# Upload File
# ===========================

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

    version = FileVersion(
        file_id=new_file.id,
        version=1,
        storage_path=new_file.storage_path,
        size=new_file.size
    )

    db.add(version)
    db.commit()

    return {
        "file_id": str(new_file.id),
        "filename": new_file.filename,
        "size": new_file.size,
        "saved_at": new_file.storage_path
    }


# ===========================
# List Files
# ===========================

@router.get("/files")
def list_files(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):

    offset = (page - 1) * limit

    files = (
        db.query(FileModel)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [
        {
            "id": str(file.id),
            "filename": file.filename,
            "size": file.size,
            "storage_path": file.storage_path
        }
        for file in files
    ]


# ===========================
# Search Files
# ===========================

@router.get("/files/search")
def search_files(
    filename: str = Query(...),
    db: Session = Depends(get_db)
):

    files = db.query(FileModel).filter(
        FileModel.filename.ilike(f"%{filename}%")
    ).all()

    return [
        {
            "id": str(file.id),
            "filename": file.filename,
            "size": file.size,
            "storage_path": file.storage_path
        }
        for file in files
    ]


# ===========================
# Download Latest Version
# ===========================

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


# ===========================
# Delete File
# ===========================

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


# ===========================
# Replace File (Create New Version)
# ===========================

@router.put("/files/{file_id}")
async def replace_file(
    file_id: str,
    file: UploadFile = File(...),
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

    new_version = file_record.current_version + 1

    _, extension = os.path.splitext(file.filename)
    new_filename = f"{file_record.id}_v{new_version}{extension}"

    new_path = os.path.join(
        STORAGE_DIR,
        new_filename
    )

    with open(new_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_size = os.path.getsize(new_path)

    file_record.filename = file.filename
    file_record.storage_path = new_path
    file_record.size = new_size
    file_record.current_version = new_version

    version = FileVersion(
        file_id=file_record.id,
        version=new_version,
        storage_path=new_path,
        size=new_size
    )

    db.add(version)
    db.commit()
    db.refresh(file_record)

    return {
        "message": "File updated successfully",
        "file_id": str(file_record.id),
        "filename": file_record.filename,
        "current_version": file_record.current_version,
        "size": file_record.size
    }


# ===========================
# Version History
# ===========================

@router.get("/files/{file_id}/versions")
def get_file_versions(
    file_id: str,
    db: Session = Depends(get_db)
):

    file = db.query(FileModel).filter(
        FileModel.id == file_id
    ).first()

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    versions = (
        db.query(FileVersion)
        .filter(FileVersion.file_id == file_id)
        .order_by(FileVersion.version.asc())
        .all()
    )

    return [
        {
            "version": version.version,
            "size": version.size,
            "storage_path": version.storage_path,
            "created_at": version.created_at
        }
        for version in versions
    ]


# ===========================
# Download Specific Version
# ===========================

@router.get("/files/{file_id}/versions/{version}/download")
def download_specific_version(
    file_id: str,
    version: int,
    db: Session = Depends(get_db)
):

    version_record = (
        db.query(FileVersion)
        .filter(
            FileVersion.file_id == file_id,
            FileVersion.version == version
        )
        .first()
    )

    if not version_record:
        raise HTTPException(
            status_code=404,
            detail="Version not found"
        )

    return FileResponse(
        path=version_record.storage_path,
        filename=os.path.basename(version_record.storage_path),
        media_type="application/octet-stream"
    )


# ===========================
# Get File Metadata
# ===========================

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
        "storage_path": file_record.storage_path,
        "current_version": file_record.current_version
    }