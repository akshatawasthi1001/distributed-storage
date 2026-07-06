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
from app.services.upload_service import upload_new_file
from app.services.file_service import (
    download_file,
    get_file_metadata,
    search_files,
    delete_file
)
from app.services.version_service import (
    replace_file,
    get_versions,
    download_version
)
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

    return upload_new_file(file, db)

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
def search(
    filename: str = Query(...),
    db: Session = Depends(get_db)
):

    return search_files(filename, db)

# ===========================
# Download Latest Version
# ===========================

@router.get("/download/{file_id}")
def download(
    file_id: str,
    db: Session = Depends(get_db)
):

    return download_file(file_id, db)


# ===========================
# Delete File
# ===========================

@router.delete("/files/{file_id}")
def delete(
    file_id: str,
    db: Session = Depends(get_db)
):

    return delete_file(file_id, db)

# ===========================
# Replace File (Create New Version)
# ===========================

@router.put("/files/{file_id}")
async def replace(
    file_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    return replace_file(
        file_id,
        file,
        db
    )
# ===========================
# Version History
# ===========================

@router.get("/files/{file_id}/versions")
def versions(
    file_id: str,
    db: Session = Depends(get_db)
):

    return get_versions(
        file_id,
        db
    )
# ===========================
# Download Specific Version
# ===========================

@router.get("/files/{file_id}/versions/{version}/download")
def version_download(
    file_id: str,
    version: int,
    db: Session = Depends(get_db)
):

    return download_version(
        file_id,
        version,
        db
    )

# ===========================
# Get File Metadata
# ===========================

@router.get("/files/{file_id}")
def file_metadata(
    file_id: str,
    db: Session = Depends(get_db)
):

    return get_file_metadata(file_id, db)